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
    email: str


def main():
    cm = ConnectionManager(**SF_CONFIG)
    db = WSnowflake(cm)

    def transaction_operations(tx):
        db.insert(User(id=2, name="Jane", email="jane@example.com"))
        return True

    result = db.with_transaction(transaction_operations)
    print(f"Transaction result: {result}")


if __name__ == "__main__":
    main()
