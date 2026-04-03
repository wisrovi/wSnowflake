Quickstart
===========

This guide will help you get started with wSnowflake quickly.

Basic Usage
-----------

.. code-block:: python

    from wSnowflake import WSnowflake, ConnectionManager

    cm = ConnectionManager(
        user="your_user",
        password="your_password",
        account="your_account",
        warehouse="your_warehouse",
        database="your_database",
        schema="your_schema"
    )

    db = WSnowflake(cm)

    result = db.fetch_all("SELECT * FROM my_table")
    print(result)

Execute Queries
---------------

.. code-block:: python

    db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, name STRING)")

    db.execute("INSERT INTO users VALUES (1, 'John')")

    result = db.fetch_all("SELECT * FROM users")

Using QueryBuilder
------------------

.. code-block:: python

    from wSnowflake import QueryBuilder

    query = (QueryBuilder()
        .select("id", "name", "email")
        .from_table("users")
        .where("active", "=", True)
        .limit(100)
        .build())

    results = db.execute(query)

Using TableSync
---------------

.. code-block:: python

    from wSnowflake import TableSync
    from pydantic import BaseModel

    class User(BaseModel):
        id: int | None = None
        name: str
        email: str

    sync = TableSync(cm)
    sync.sync_table(User, "users")