from fastapi import HTTPException
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from auth.manager import get_user_manager
from auth.models import User
from config import SECRET_AUTH

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

async def get_current_user(token: str):
    try:
        user = await get_jwt_strategy().get_current_user(token=token)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user