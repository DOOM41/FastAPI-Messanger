from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from chats import crud
from auth import schemas
from auth.base_config import current_user

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.get("/")
async def create_chat(
    now_user: Annotated[schemas.UserRead, Depends(current_user)],
    user_id,
    session: AsyncSession = Depends(get_async_session)
):
    chats = crud.get_chats_by_user(
        db=session,
        user=now_user
    )
    if chats:
        return {"res": 'existed'}
    chat = crud.create_chat(
        session,
        current_user.id,
        user_id
    )
    return chat


# @router.post("/")
# async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
#     stmt = insert(operation).values(**new_operation.dict())
#     await session.execute(stmt)
#     await session.commit()
#     return {"status": "success"}
