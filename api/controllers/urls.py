from .main import (
    app,
)
from .messages import send_message, get_message
from . import user
from ..schemas import schemas

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
    '/users/{chat_id}',
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
    '/send_message/{to_user_id}',
    send_message,
    methods=['post']
)
app.add_api_route(
    '/get_my_mes',
    get_message,
    methods=['get']
)
