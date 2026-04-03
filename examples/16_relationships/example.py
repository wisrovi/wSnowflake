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


class Author(BaseModel):
    id: int
    name: str


class Book(BaseModel):
    id: int
    title: str
    author_id: int


def main():
    cm = ConnectionManager(**SF_CONFIG)
    author_db = WSnowflake(cm)
    book_db = WSnowflake(cm)

    author_db.insert(Author(id=1, name="Alice"))
    book_db.insert(Book(id=1, title="Book 1", author_id=1))

    print(f"Authors: {author_db.get_all()}")
    print(f"Books: {book_db.get_all()}")


if __name__ == "__main__":
    main()
