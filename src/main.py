import asyncio
import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate, UserUpdate

from chats.chat_router import router as router_chats
from chats.message_roter import router as router_messages

import uvicorn

from database import create_db_and_tables

app = FastAPI(
    title="Message App"
)


origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(
        auth_backend
    ),
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


sio = socketio.Server(async_mode='asgi')
app.mount('/socket.io', socketio.ASGIApp(sio))
@sio.on('message')
async def handle_message(sid, data):
    print('Received message:', data)
    await sio.emit('response', 'Received message: ' + data)


app.include_router(router_chats)
app.include_router(router_messages)

if __name__ == '__main__':
    asyncio.run(create_db_and_tables())
    uvicorn.run(
        app,
        host='172.28.0.224',
    )
