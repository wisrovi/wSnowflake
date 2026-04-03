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


class Product(BaseModel):
    id: int
    name: str
    price: float


def main():
    cm = ConnectionManager(**SF_CONFIG)
    db = WSnowflake(cm, table_name="products")
    db.sync.create_if_not_exists()

    products = [
        Product(id=1, name="Laptop", price=999.99),
        Product(id=2, name="Mouse", price=29.99),
        Product(id=3, name="Keyboard", price=89.99),
    ]
    for p in products:
        db.insert(p)

    result = db.execute_raw("SELECT * FROM products WHERE price > (SELECT AVG(price) FROM products)")
    print(f"Above average: {result}")

    cm.close()


if __name__ == "__main__":
    main()