from typing import Any, List, Dict

import aiohttp


from .models import User, CreateUserParams


class UserRepository:
    """Class that processes all requests connected with posts."""
    def __init__(self):
        self._users_endpoint = 'https://jsonplaceholder.typicode.com/users'

    async def create_user(self, user: CreateUserParams) -> User:
        """Method that creates a user.
        Args:
            user: Parameters based on which the post will be created.
        Returns:
            New user that was created.
        """
        raw_user = await self._create_user(user)
        return self._convert_user(raw_user)

    async def list_users(self) -> List[User]:
        """Method that gets all users from remote repository.
        Returns:
            List of received users.
        """
        raw_users = await self._list_users()
        return [self._convert_user(raw_user) for raw_user in raw_users]

    async def _create_user(self, user: CreateUserParams) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            resp = await session.post(self._users_endpoint, json=user.dict())
            raw_user = await resp.json()
            return raw_user

    async def _list_users(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self._users_endpoint)
            raw_users = await resp.json()

            return raw_users

    def _convert_user(self, raw_user: Dict[str, Any]) -> User:
        return User(**raw_user)


class UserRepositoryFactory:
    """Class factory that creates UserRepository object"""
    def __init__(self):
        self._repo = None

    def __call__(self) -> UserRepository:
        if self._repo is None:
            self._repo = UserRepository()
        return self._repo


get_user_storage = UserRepositoryFactory()
