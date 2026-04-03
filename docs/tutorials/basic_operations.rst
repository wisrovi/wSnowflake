Basic Operations
=================

This tutorial covers basic database operations with wSnowflake.

Setup
-----

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

Execute Queries
---------------

.. code-block:: python

    db.execute("CREATE TABLE IF NOT EXISTS sales (id INTEGER, amount DOUBLE, date DATE)")

    db.execute("INSERT INTO sales VALUES (1, 100.50, '2024-01-01')")

Fetch Results
-------------

.. code-block:: python

    rows = db.fetch_all("SELECT * FROM sales")
    for row in rows:
        print(row)

    row = db.fetch_one("SELECT * FROM sales WHERE id = 1")

Parameterized Queries
--------------------

.. code-block:: python

    rows = db.fetch_all(
        "SELECT * FROM sales WHERE amount > ?",
        params=(50,)
    )