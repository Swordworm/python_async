from fastapi import APIRouter, Depends
from typing import List

from .dependencies import get_user_storage, UserRepository
from .models import User, CreateUserParams

router = APIRouter(
    prefix='/users'
)


@router.get("/", tags=["users"], response_model=List[User])
async def list_users(
        repository: UserRepository = Depends(get_user_storage)
) -> List[User]:
    """Get all posts from repository.

    Args:
        repository: Repository from where we take data.
    Returns:
        Returns list of User objects.
    """
    users = await repository.list_users()
    return users


@router.post("/new", tags=["users"], response_model=User, status_code=201)
async def create_user(
    user: CreateUserParams,
    repository: UserRepository = Depends(get_user_storage)
) -> User:
    """Get all posts from repository.

    Args:
        user: Params that are converted into User object.
        repository: Repository from where we take data.
    Returns:
        Returns list of User objects.
    """
    user = await repository.create_user(user)
    return user
