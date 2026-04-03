class WSnowflakeError(Exception):
    """Base exception for all wSnowflake errors."""

    pass


class ConnectionError(WSnowflakeError):
    """Raised when connection to Snowflake fails."""

    pass


class QueryError(WSnowflakeError):
    """Raised when query execution fails."""

    pass


class ValidationError(WSnowflakeError):
    """Raised when validation fails."""

    pass


class TransactionError(WSnowflakeError):
    """Raised when transaction operations fail."""

    pass


class TableSyncError(WSnowflakeError):
    """Raised when table synchronization fails."""

    pass


class OperationError(WSnowflakeError):
    """Raised when database operation fails."""

    pass
