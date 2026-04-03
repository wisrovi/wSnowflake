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
    id: int = Field(..., description="Primary Key")
    name: str = Field(..., description="NOT NULL")
    email: Optional[str] = Field(None, description="UNIQUE")


def main():
    cm = ConnectionManager(**SF_CONFIG)
    db = WSnowflake(cm)

    print("=== INSERT VALID ===")
    db.insert(User(id=1, name="Alice", email="alice@example.com"))
    print(f"Count: {db.count()}")

    print("\n=== UNIQUE VIOLATION ===")
    try:
        db.insert(User(id=2, name="Bob", email="alice@example.com"))
    except Exception as e:
        print(f"Error: {e}")

    print("\n=== INSERT MORE ===")
    db.insert(User(id=2, name="Bob", email="bob@example.com"))
    print(f"Count: {db.count()}")


if __name__ == "__main__":
    main()
