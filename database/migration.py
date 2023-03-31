from models import (
    Base,
)
from db import engine

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

    # admin = User(username='admin', password='fastapi', mail='root@root.com')
    