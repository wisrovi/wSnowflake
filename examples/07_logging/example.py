import logging
from pydantic import BaseModel
from wSnowflake import WSnowflake, ConnectionManager

logging.basicConfig(level=logging.DEBUG)

SF_CONFIG = {
    "user": "your_user",
    "password": "your_password",
    "account": "your_account",
    "warehouse": "your_warehouse",
    "database": "your_database",
    "schema": "your_schema",
}


class User(BaseModel):
    id: int
    name: str
    email: str


def main():
    cm = ConnectionManager(**SF_CONFIG)
    db = WSnowflake(cm, log_level=logging.DEBUG)
    db.sync.create_if_not_exists()

    db.insert(User(id=1, name="LoggedUser", email="logged@example.com"))
    print("Logged operation completed")

    cm.close()


if __name__ == "__main__":
    main()