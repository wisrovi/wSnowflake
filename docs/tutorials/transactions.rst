Transactions
============

Transaction management in wSnowflake.

Note: Snowflake handles transactions differently from traditional RDBMS. 
Review Snowflake transaction documentation for specific behavior.

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

    try:
        db.execute("BEGIN")
        db.execute("INSERT INTO logs VALUES (1, 'action1')")
        db.execute("INSERT INTO logs VALUES (2, 'action2')")
        db.execute("COMMIT")
    except Exception as e:
        db.execute("ROLLBACK")
        raise e

Using Context Manager
---------------------

.. code-block:: python

    from wSnowflake import Transaction

    with Transaction(cm) as t:
        db = WSnowflake(t)
        db.execute("INSERT INTO logs VALUES (1, 'test')")
        db.execute("INSERT INTO logs VALUES (2, 'test2')")

Multi-statement Transactions
---------------------------

.. code-block:: python

    db.execute("""
        BEGIN;
        INSERT INTO table1 VALUES (1);
        INSERT INTO table2 VALUES (2);
        COMMIT;
    """)