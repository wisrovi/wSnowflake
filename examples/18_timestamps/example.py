from datetime import datetime
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


class Record(BaseModel):
    id: int
    data: str
    created_at: str = datetime.now().isoformat()


def main():
    cm = ConnectionManager(**SF_CONFIG)
    db = WSnowflake(cm)
    db.insert(Record(id=1, data="Test"))
    record = db.get_by_field(id=1)[0]
    print(f"Record: {record}")


if __name__ == "__main__":
    main()
