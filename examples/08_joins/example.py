from pydantic import BaseModel
from wSnowflake import WSnowflake, ConnectionManager, QueryBuilder

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


class Order(BaseModel):
    id: int
    user_id: int
    amount: float


def main():
    cm = ConnectionManager(**SF_CONFIG)
    db_user = WSnowflake(cm, table_name="users")
    db_order = WSnowflake(cm, table_name="orders")

    db_user.sync.create_if_not_exists()
    db_order.sync.create_if_not_exists()

    db_user.insert(User(id=1, name="John", email="john@example.com"))
    db_order.insert(Order(id=1, user_id=1, amount=100.0))

    query = (
        QueryBuilder()
        .select("u.name", "o.amount")
        .from_table("users", "u")
        .join("orders", "o", "u.id = o.user_id")
        .build()
    )
    print(f"Join query: {query}")

    cm.close()


if __name__ == "__main__":
    main()