from typing import Annotated

from fastapi import APIRouter, Depends, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from auth import schemas
from auth.base_config import current_user,get_current_user
from auth.crud import get_user

from chats import crud, models
from chats.schemas import ChatList, MessageList, MessageSendSchema
from chats.utils import check_user_in_chat


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("/create/{user_id}")
async def create_chat(
    now_user: Annotated[schemas.UserRead, Depends(current_user)],
    user_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    user = await get_user(session, user_id)
    chats = await crud.get_chats_by_users(
        db=session,
        cur_user=now_user,
        to_user=user
    )
    if len(chats) > 0:
        return {"res": 'existed'}
    chat = await crud.create_chat(
        session,
        now_user.id,
        user_id
    )
    return chat


@router.get("/my")
async def get_own_chats(
    current_user: Annotated[schemas.UserRead, Depends(current_user)],
    session: AsyncSession = Depends(get_async_session)
):
    chats = await crud.get_chats_by_user(
        db=session,
        cur_user=current_user,
    )
    return ChatList(
        chats=chats
    )


@router.get("/{chat_id}")
async def get_messages(
    current_user: Annotated[schemas.UserRead, Depends(current_user)],
    chat_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    await check_user_in_chat(session, current_user, chat_id)
    messages = await crud.get_messages_by_chat_id(
        session,
        chat_id
    )
    return MessageList(messages=messages)


@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    breakpoint()
    await websocket.accept()
    token = await websocket.receive()
    current_user = get_current_user(token)
    await check_user_in_chat(session, current_user, chat_id)
    while True:
        data: MessageSendSchema = await websocket.receive_json()
        message = await crud.create_user_message(
            db=session,
            mess=data,
            chat_id=chat_id,
            user=current_user
        )
        messages = await crud.get_messages_by_chat_id(
            session,
            chat_id
        )
        await websocket.send_json(
            message
        )

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


@router.post("/{chat_id}/send_message")
async def send_messages(
    current_user: Annotated[schemas.UserRead, Depends(current_user)],
    chat_id: int,
    mess: MessageSendSchema,
    session: AsyncSession = Depends(get_async_session)
):
    await check_user_in_chat(session, current_user, chat_id)
    message = await crud.create_user_message(
        db=session,
        mess=mess,
        chat_id=chat_id,
        user=current_user
    )
    return {'res': 'sended'}
