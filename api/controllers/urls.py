from .main import (
    app,
)
from ..schemas import schemas

from . import messages
from . import user

app.add_api_route(
    '/users',
    user.create_user,
    methods=['post'],
    response_model=schemas.User,
    tags=['user']
)
app.add_api_route(
    '/users/login',
    user.login_for_access_token,
    methods=['post'],
    response_model=schemas.Token,
    tags=['user']
)
app.add_api_route(
    '/users/me',
    user.read_users_me,
    methods=['get'],
    response_model=schemas.User,
    tags=['user']
)
app.add_api_route(
    '/users/{user_id}',
    user.read_user,
    methods=['get'],
    response_model=schemas.User,
    tags=['user']
)
app.add_api_route(
    '/users',
    user.read_users,
    methods=['get'],
    response_model=list[schemas.User],
    tags=['user']
)



app.add_api_route(
    '/chat/{user_id}',
    messages.create_chat,
    methods=['post'],
    tags=['chats']
)
app.add_api_route(
    '/chat/my',
    messages.get_own_chats,
    methods=['get'],
    tags=['chats']
)

app.add_api_route(
    '/send_message/{chat_id}',
    messages.send_message,
    methods=['post'],
    tags=['messages']
)

app.add_api_route(
    '/get_data/{chat_id}',
    messages.get_messages,
    methods=['get'],
    tags=['messages']
)