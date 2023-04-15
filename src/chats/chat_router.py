from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session

from auth import schemas
from auth.base_config import current_user
from auth.crud import get_user

from chats import crud
from chats.schemas import ChatList, MessageList, MessageSendSchema
from chats.utils import (
    check_user_in_chat,
    check_user_in_chat_ws,
    check_chat_existed
)
from chats.conections import manager

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
    chat = await crud.get_chat(session, chat_id)
    await check_user_in_chat(session, current_user, chat_id)
    await check_chat_existed(chat)
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
    # Connect ws
    await manager.connect(websocket)
    first_data = await websocket.receive_json()

    # Chekers
    chat = await crud.get_chat(session, chat_id)
    user = await get_user(
        session,
        first_data['from_user_id']
    )
    await check_user_in_chat(session, current_user, chat_id)
    await check_chat_existed(chat, is_ws=True)
    await check_user_in_chat_ws(
        session, user, chat_id
    )
    try:
        while True:
            message_f = await websocket.receive_json()
            message = await crud.create_user_message(
                db=session,
                mess=message_f,
                chat=chat,
                user=user
            )
            new_data = MessageSendSchema(
                content=message.content,
                date_stamp=message.date.timestamp()
            ).dict()
            await manager.send_not_message(
                new_data,
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except HTTPException as e:
        manager.disconnect(websocket)
        await manager.send_personal_message(
            "This user not in this chat", websocket
        )
