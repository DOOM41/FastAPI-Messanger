from database import db
from database.models import User

from ..schemas.schemas import UserSchema

from sqlalchemy.exc import IntegrityError


async def register_acc(user: UserSchema):
    try:
        new_user = User(user.username, user.password, user.mail)
        db.session.add(new_user)
        db.session.commit()
        return {
            'result': "Created"
        }
    except IntegrityError as e:
        return {
            'result': f"Existed {e}"
        }

