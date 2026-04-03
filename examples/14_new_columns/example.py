from typing import Optional
from pydantic import BaseModel
from wSnowflake import WSnowflake, ConnectionManager

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
    age: int


def main():
    cm = ConnectionManager(**SF_CONFIG)
    db = WSnowflake(cm)
    db.insert(User(id=1, name="Alice", age=25))
    print(f"Initial users: {db.get_all()}")


class UserExtended(BaseModel):
    id: int
    name: str
    age: int
    email: Optional[str] = None


def main_extended():
    cm = ConnectionManager(**SF_CONFIG)
    db = WSnowflake(cm)
    db.insert(UserExtended(id=2, name="Bob", age=30, email="bob@example.com"))
    print(f"Users with new column: {db.get_all()}")


if __name__ == "__main__":
    main()
