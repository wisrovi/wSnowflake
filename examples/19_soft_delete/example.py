from typing import Optional
from pydantic import BaseModel, Field
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
    deleted: Optional[int] = Field(default=0)


def main():
    cm = ConnectionManager(**SF_CONFIG)
    db = WSnowflake(cm)

    db.insert(User(id=1, name="Alice"))
    db.insert(User(id=2, name="Bob"))

    print(f"Total: {db.count()}")
    user = db.get_by_field(id=1)[0]
    db.update(1, User(id=1, name=user.name, deleted=1))
    print(f"After soft delete: {db.count()}")


if __name__ == "__main__":
    main()
