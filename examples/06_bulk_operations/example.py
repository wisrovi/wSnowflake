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

    users = [
        User(id=i, name=f"BulkUser{i}", email=f"bulk{i}@example.com")
        for i in range(1, 11)
    ]
    db.bulk_insert(users)
    print(f"Bulk inserted {len(users)} users")

    db.bulk_update(users)
    print("Bulk updated users")

    cm.close()


if __name__ == "__main__":
    main()