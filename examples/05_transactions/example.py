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
    db.sync.create_if_not_exists()

    db.insert(User(id=1, name="Alice", email="alice@example.com"))

    def transactional_op(tx):
        db.update(User(id=1, name="Alice Updated", email="alice.updated@example.com"))
        return True

    result = db.with_transaction(transactional_op)
    print(f"Transaction result: {result}")

    cm.close()


if __name__ == "__main__":
    main()