from models import (
    SQLITE3_NAME,
    User,
    create_db_and_tables
)

import os

if __name__ == "__main__":
    path = SQLITE3_NAME
    if not os.path.isfile(path):

        # create new table
        create_db_and_tables

    admin = User(username='admin', password='fastapi', mail='root@root.com')
    