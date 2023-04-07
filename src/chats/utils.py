# FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.exceptions import HTTPException

# APPS
from chats.models import Chat
from chats import crud
from auth.models import User


async def check_user_in_chat(
        session: AsyncSession,
        current_user: User,
        chat_id: int
):
    chat: Chat = await crud.get_chat(session, chat_id)
    if not chat:
        raise HTTPException(
            status_code=400,
            detail={'res': 'Chat didnt existed'}
        )
    elif current_user.id != chat.from_id and current_user.id != chat.to_id:
        raise HTTPException(
            status_code=400,
            detail={'res': 'You are not in this chat'}
        )
    return 