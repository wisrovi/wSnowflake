from pydantic import BaseModel
from wSnowflake import WSnowflake, ConnectionManager, TableSync

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
    ts = TableSync(cm, User, "users")
    ts.create_if_not_exists()
    print("Table synced")


if __name__ == "__main__":
    main()
