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

    for i in range(1, 21):
        db.insert(User(id=i, name=f"User{i}", email=f"user{i}@example.com"))

    page1 = db.paginate(page=1, page_size=5)
    print(f"Page 1: {len(page1)} users")

    page2 = db.paginate(page=2, page_size=5)
    print(f"Page 2: {len(page2)} users")

    cm.close()


if __name__ == "__main__":
    main()