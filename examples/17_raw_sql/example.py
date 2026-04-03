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


def main():
    cm = ConnectionManager(**SF_CONFIG)
    db = WSnowflake(cm)
    db.insert(User(id=1, name="Alice"))

    result = db.execute_raw("SELECT COUNT(*) as cnt FROM user")
    print(f"Count: {result}")


if __name__ == "__main__":
    main()
