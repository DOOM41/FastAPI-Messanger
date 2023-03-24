from sqlalchemy.orm import Query
from database import db
from database.models import User, Message, get_user_db

from ..schemas.schemas import MessageSchema, UserSchema
from sqlalchemy import and_, or_


async def send_message(message: MessageSchema):
    user = get_user_db()
    breakpoint()
    check_u = user.session.filter(
        User.id == message.from_user
    ).first()
    check_u_2 = get_user_db().query(User).filter(
        User.id == message.to_user
    ).first()
    if not check_u or not check_u_2:
        return {"result": 'Not Existed'}
    new_mess = Message(
        from_user_id=message.from_user,
        to_user_id=message.to_user,
        content=message.content,
    )
    db.session.add(new_mess)
    db.session.commit()
    return {
        'result': "sended"
    }


async def get_message(first_id: int, second_id: int):
    # user1 = UserSchema.from_orm()
    user2 = UserSchema.from_orm(db.async_session_maker.query(User).get(second_id))
    my_messages: Query[Message] = db.session.query(Message).filter(
        or_(
            and_(
                Message.from_user_id == first_id,
                Message.to_user_id == second_id
            ),
            and_(
                Message.from_user_id == second_id,
                Message.to_user_id == first_id
            ),
        )
    ).all()
    messages = []
    for message in my_messages:
        message_dict = {
            'from_user': message.from_user_id,
            'to_user': message.to_user_id,
            'content': message.content,
            'date': message.date
        }
        messages.append(MessageSchema(**message_dict))
    return {
        'result': messages,
        'users': [user1.dict(), user2.dict()]
    }

