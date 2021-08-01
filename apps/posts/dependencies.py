from typing import Any, List, Dict

import aiohttp
from fastapi import Depends

from .models import Post, CreatePostParams, EditPostParams


class PostRepository:
    """Class that processes all requests connected with posts."""
    def __init__(self, session):
        self._session = session
        self._posts_endpoint = 'https://jsonplaceholder.typicode.com/posts'
        self._users_endpoint = 'https://jsonplaceholder.typicode.com/users'
        self._comments_endpoint = 'https://jsonplaceholder.typicode.com/comments'

    @property
    def session(self):
        return self._session

    async def create_post(self, post: CreatePostParams) -> Post:
        """Method that creates a post.
        Args:
            post: Parameters based on which the post will be created.
        Returns:
            New post that was created.
        """
        raw_post = await self._create_post(post)
        await self._get_user(raw_post)
        return self._convert_post(raw_post)

    async def list_posts(self) -> List[Post]:
        """Method that gets all posts from remote repository.
        Returns:
            List of received posts.
        """
        raw_posts = await self._list_posts()
        return [self._convert_post(raw_post) for raw_post in raw_posts]

    async def single_post(self, post_id: str) -> Post:
        """Method that gets detailed data about a single post.
        Args:
            post_id: ID of a post.
        Returns:
            Detailed post with comments.
        """
        raw_post = await self._single_post(post_id)
        return self._convert_post(raw_post)

    async def edit_post(self, post_id: str, edited_params: EditPostParams) -> Post:
        """Method that edits post by id.
        Args:
            post_id: ID of chosen post.
            edited_params: Edited parameters that will be changed.
        Returns:
            Edited post.
        """
        raw_post = await self._edit_post(post_id, edited_params)
        return self._convert_post(raw_post)

    async def _create_post(self, post: CreatePostParams) -> Dict[str, Any]:
        resp = await self.session.post(self._posts_endpoint, json=post.dict())
        raw_post = await resp.json()
        return raw_post

    async def _list_posts(self) -> List[Dict[str, Any]]:
        posts = await self.session.get(self._posts_endpoint)
        raw_posts = await posts.json()
        for raw_post in raw_posts:
            await self._get_user(raw_post)

        return raw_posts

    async def _single_post(self, post_id: str) -> Dict[str, Any]:
        resp = await self.session.get(f'{self._posts_endpoint}/{post_id}')
        raw_post = await resp.json()
        await self._get_user(raw_post)
        await self._get_comments(raw_post)

        return raw_post

    async def _edit_post(self, post_id: str, edited_params: EditPostParams) -> Dict[str, Any]:
        resp = await self.session.patch(f'{self._posts_endpoint}/{post_id}', json=edited_params.dict())
        raw_post = await resp.json()
        await self._get_user(raw_post)
        await self._get_comments(raw_post)

        return raw_post

    async def _get_user(self, raw_post: Dict[str, Any]):
        data = await self.session.get(f'{self._users_endpoint}/{raw_post["userId"]}')
        user = await data.json()
        await self._attach_user_to_post(raw_post, user)

    async def _get_comments(self, raw_post):
        data = await self.session.get(
            self._comments_endpoint,
            params={
                'postId': raw_post['id']
            }
        )
        comments = await data.json()
        raw_post['comments'] = comments

    async def _attach_user_to_post(self, raw_post, user):
        raw_post.pop('userId')
        raw_post['user'] = {}
        raw_post['user']['id'] = user['id']
        raw_post['user']['name'] = user['name']
        raw_post['user']['email'] = user['email']

    def _convert_post(self, raw_post: Dict[str, Any]) -> Post:
        return Post(**raw_post)


async def get_session():
    async with aiohttp.ClientSession() as session:
        yield session


class PostRepositoryFactory:
    """Class factory that creates PostRepository object"""
    def __init__(self):
        self._repo = None

    async def __call__(self, session: aiohttp.ClientSession = Depends(get_session)) -> PostRepository:
        if self._repo is None:
            self._repo = PostRepository(session)
        return self._repo


get_post_storage = PostRepositoryFactory()


