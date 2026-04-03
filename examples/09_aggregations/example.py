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


class Order(BaseModel):
    id: int
    user_id: int
    amount: float


def main():
    cm = ConnectionManager(**SF_CONFIG)
    db = WSnowflake(cm, table_name="orders")
    db.sync.create_if_not_exists()

    for i in range(1, 6):
        db.insert(Order(id=i, user_id=i, amount=float(i * 10)))

    total = db.aggregate("SUM", "amount")
    print(f"Total: {total}")

    count = db.aggregate("COUNT", "id")
    print(f"Count: {count}")

    avg = db.aggregate("AVG", "amount")
    print(f"Average: {avg}")

    cm.close()


if __name__ == "__main__":
    main()