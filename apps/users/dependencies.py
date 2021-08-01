from typing import Any, List, Dict

import aiohttp
from fastapi import Depends

from .models import User, CreateUserParams


class UserRepository:
    """Class that processes all requests connected with posts."""
    def __init__(self, session):
        self._session = session
        self._users_endpoint = 'https://jsonplaceholder.typicode.com/users'

    @property
    def session(self):
        return self._session

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
        resp = await self.session.post(self._users_endpoint, json=user.dict())
        raw_user = await resp.json()
        return raw_user

    async def _list_users(self) -> List[Dict[str, Any]]:
        resp = await self.session.get(self._users_endpoint)
        raw_users = await resp.json()

        return raw_users

    def _convert_user(self, raw_user: Dict[str, Any]) -> User:
        return User(**raw_user)


async def get_session():
    async with aiohttp.ClientSession() as session:
        yield session


class UserRepositoryFactory:
    """Class factory that creates UserRepository object"""
    def __init__(self):
        self._repo = None

    async def __call__(self, session: aiohttp.ClientSession = Depends(get_session)) -> UserRepository:
        if self._repo is None:
            self._repo = UserRepository(session)
        return self._repo


get_user_storage = UserRepositoryFactory()
