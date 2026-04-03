FAQ
===

Frequently Asked Questions about wSnowflake.

General
-------

What is wSnowflake?
~~~~~~~~~~~~~~~~~~~

wSnowflake is a Python ORM library for Snowflake providing connection management, query building, and CRUD operations with Snowflake SQL support.

What Python versions are supported?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wSnowflake supports Python 3.8 and later.

Connection
----------

How do I configure the connection?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wSnowflake import ConnectionManager

    cm = ConnectionManager(
        user="your_user",
        password="your_password",
        account="your_account",
        warehouse="your_warehouse",
        database="your_database",
        schema="your_schema"
    )

What is the account format?
~~~~~~~~~~~~~~~~~~~~~~~~~~

The account format is your organization-specific identifier, e.g., ``xy12345.us-east-1``.

Where do I find my credentials?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In Snowflake, go to Account -> Users to manage user credentials.

Transactions
------------

How do I use transactions?
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wSnowflake import Transaction

    with Transaction(cm) as t:
        db = WSnowflake(t)
        db.execute("INSERT INTO logs VALUES (1, 'test')")

Are all operations transactional?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most DML operations can be wrapped in transactions. Some operations like DDL may auto-commit.

Errors
------

What exceptions does wSnowflake raise?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``WSnowflakeError`` - Base exception
- ``ConnectionError`` - Connection failures
- ``QueryError`` - Query execution errors
- ``ValidationError`` - Data validation errors
- ``TransactionError`` - Transaction failures
- ``TableSyncError`` - Table synchronization errors
- ``OperationError`` - General operation errors