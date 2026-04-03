"""wSnowflake - Snowflake SQL ORM Library.

A production-ready ORM for Snowflake that provides connection management,
query building, schema synchronization, and CRUD operations.

Usage:
    from wSnowflake import WSnowflake, ConnectionManager

    cm = ConnectionManager(
        user='your_user',
        password='your_password',
        account='your_account',
        warehouse='your_warehouse',
        database='your_database',
        schema='your_schema',
    )

    db = WSnowflake(cm)
    result = db.fetch_all('my_table')

Async usage:
    from wSnowflake import AsyncConnectionManager, AsyncWSnowflake

    async with AsyncConnectionManager(...) as cm:
        db = AsyncWSnowflake(cm)
        results = await db.fetch_all_async('my_table')
"""

from wSnowflake.builders import QueryBuilder
from wSnowflake.core.connection import ConnectionManager
from wSnowflake.core.repository import WSnowflake
from wSnowflake.core.sync import TableSync
from wSnowflake.exceptions import (
    ConnectionError,
    OperationError,
    QueryError,
    TableSyncError,
    TransactionError,
    ValidationError,
    WSnowflakeError,
)

__version__ = "1.0.0"

__all__ = [
    "WSnowflake",
    "QueryBuilder",
    "ConnectionManager",
    "TableSync",
    "WSnowflakeError",
    "ConnectionError",
    "QueryError",
    "ValidationError",
    "TransactionError",
    "TableSyncError",
    "OperationError",
]
