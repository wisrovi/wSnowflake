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


def main():
    cm = ConnectionManager(**SF_CONFIG)
    db = WSnowflake(cm, table_name="users")
    db.sync.create_if_not_exists()

    db.insert(User(id=1, name="John", email="john@example.com"))
    db.insert(User(id=2, name="Jane", email="jane@example.com"))

    subquery = QueryBuilder().select("MAX(id)").from_table("users").build()
    query = (
        QueryBuilder()
        .select("*")
        .from_table("users")
        .where(f"id = ({subquery})")
        .build()
    )
    print(f"Subquery: {query}")

    cm.close()


if __name__ == "__main__":
    main()