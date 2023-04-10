from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate, UserUpdate
from auth import crud
from database import get_async_session
from auth.schemas import UserList


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


router.include_router(
    fastapi_users.get_auth_router(
        auth_backend
    ),
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
router.include_router(
    fastapi_users.get_reset_password_router(),
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)


@router.get('/users/')
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session)
):
    users = await crud.get_users(db, skip, limit)
    return UserList(users=users)
