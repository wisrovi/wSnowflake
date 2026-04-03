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


class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float


def main():
    cm = ConnectionManager(**SF_CONFIG)
    db = WSnowflake(cm, table_name="employees")
    db.sync.create_if_not_exists()

    employees = [
        Employee(id=1, name="Alice", department="IT", salary=70000),
        Employee(id=2, name="Bob", department="IT", salary=75000),
    ]
    for emp in employees:
        db.insert(emp)

    result = db.execute_raw(
        "SELECT name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC) as rn FROM employees"
    )
    print(f"Window function: {result}")

    cm.close()


if __name__ == "__main__":
    main()