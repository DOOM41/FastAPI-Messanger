import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from database import create_db_and_tables

from auth.auth_routers import router as router_auth

from chats.chat_router import router as router_chats
from chats.message_roter import router as router_messages


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

app.include_router(router_auth)
app.include_router(router_chats)
app.include_router(router_messages)

if __name__ == '__main__':
    asyncio.run(create_db_and_tables())
    uvicorn.run(
        app,
    )
