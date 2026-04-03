Advanced Queries
=================

Advanced query patterns with wSnowflake.

QueryBuilder
------------

.. code-block:: python

    from wSnowflake import QueryBuilder

    query = (QueryBuilder()
        .select("s.id", "s.amount", "c.name")
        .from_table("sales", "s")
        .join("customers", "c", "s.customer_id = c.id")
        .where("s.amount", ">", 100)
        .order_by("s.amount", "DESC")
        .limit(50)
        .build())

    results = db.execute(query)

Aggregations
------------

.. code-block:: python

    query = (QueryBuilder()
        .select("COUNT(*)", "SUM(amount)", "AVG(amount)", "MAX(amount)")
        .from_table("sales")
        .build())

    result = db.execute(query)

Window Functions
-----------------

.. code-block:: python

    query = (QueryBuilder()
        .select(
            "id",
            "amount",
            "SUM(amount) OVER (PARTITION BY customer_id ORDER BY date) as running_total"
        )
        .from_table("sales")
        .build())

Subqueries
----------

.. code-block:: python

    query = (QueryBuilder()
        .select("*")
        .from_table("sales")
        .where_in("customer_id",
            QueryBuilder()
            .select("id")
            .from_table("customers")
            .where("tier", "=", "premium")
            .build()
        )
        .build())