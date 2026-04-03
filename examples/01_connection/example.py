from wSnowflake import ConnectionManager

SF_CONFIG = {
    "user": "your_user",
    "password": "your_password",
    "account": "your_account",
    "warehouse": "your_warehouse",
    "database": "your_database",
    "schema": "your_schema",
}


def main():
    cm = ConnectionManager(**SF_CONFIG)
    with cm.get_connection() as conn:
        print(f"Connected: {conn is not None}")
    cm.close()


if __name__ == "__main__":
    main()
