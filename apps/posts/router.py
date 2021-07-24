from fastapi import APIRouter, Depends
from typing import List

from .dependencies import get_post_storage, PostRepository
from .models import Post, CreatePostParams, EditPostParams

router = APIRouter(
    prefix='/posts'
)


@router.get("/", tags=["posts"], response_model=List[Post])
async def list_posts(
        repository: PostRepository = Depends(get_post_storage)
) -> List[Post]:
    """Get all posts from repository.

    Args:
        repository: Repository from where we take data.
    Returns:
        Returns list of Post objects.
    """
    posts = await repository.list_posts()
    return posts


@router.post("/new", tags=["posts"], response_model=Post, status_code=201)
async def create_post(
    post: CreatePostParams,
    repository: PostRepository = Depends(get_post_storage)
) -> Post:
    """Create post depending on params.

        Args:
            post: Params that are converted into Post object.
            repository: Repository where we send new Post.
        Returns:
            Returns list of Post objects.
    """
    post = await repository.create_post(post)
    return post


@router.get("/{post_id}", tags=["posts"], response_model=Post)
async def single_post(
        post_id: str,
        repository: PostRepository = Depends(get_post_storage)
) -> Post:
    """Get detailed data for a single post.

        Args:
            post_id: Id of post that we want to get.
            repository: Repository from where we get a single post.
        Returns:
            Returns a Post object.
    """
    post = await repository.single_post(post_id)
    return post


@router.patch("/{post_id}/edit", tags=["posts"], response_model=Post)
async def edit_post(
        post_id: str,
        edited_params: EditPostParams,
        repository: PostRepository = Depends(get_post_storage)
) -> Post:
    """Get detailed data for a single post.

        Args:
            post_id: Id of post that we want to get.
            edited_params: Params that are edited for each Post object.
            repository: Repository where we send edited data.
        Returns:
            Returns a Post object.
    """
    post = await repository.edit_post(post_id, edited_params)
    return post

