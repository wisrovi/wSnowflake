from datetime import date, datetime, time
from decimal import Decimal
from typing import Any, Dict, List, Optional


class SnowflakeType:
    """Snowflake SQL data types."""

    STRING = "STRING"
    TEXT = "TEXT"
    VARCHAR = "VARCHAR"
    CHAR = "CHAR"
    NUMBER = "NUMBER"
    DECIMAL = "DECIMAL"
    NUMERIC = "NUMERIC"
    INTEGER = "INTEGER"
    INT = "INT"
    BIGINT = "BIGINT"
    SMALLINT = "SMALLINT"
    FLOAT = "FLOAT"
    FLOAT8 = "FLOAT8"
    DOUBLE = "DOUBLE"
    REAL = "REAL"
    BOOLEAN = "BOOLEAN"
    BOOL = "BOOL"
    DATE = "DATE"
    DATETIME = "DATETIME"
    TIMESTAMP = "TIMESTAMP"
    TIMESTAMP_LTZ = "TIMESTAMP_LTZ"
    TIMESTAMP_NTZ = "TIMESTAMP_NTZ"
    TIMESTAMP_TZ = "TIMESTAMP_TZ"
    TIME = "TIME"
    BINARY = "BINARY"
    VARBINARY = "VARBINARY"
    BLOB = "BLOB"
    ARRAY = "ARRAY"
    VARIANT = "VARIANT"
    OBJECT = "OBJECT"
    GEOGRAPHY = "GEOGRAPHY"
    GEOMETRY = "GEOMETRY"


PYTHON_TO_SNOWFLAKE: Dict[type, str] = {
    str: "VARCHAR(16777216)",
    int: "NUMBER(38, 0)",
    float: "FLOAT",
    bool: "BOOLEAN",
    bytes: "BINARY",
    bytearray: "BINARY",
    datetime: "TIMESTAMP_NTZ",
    date: "DATE",
    time: "TIME",
    Decimal: "DECIMAL(38, 10)",
    list: "ARRAY",
    dict: "OBJECT",
    type(None): "VARCHAR(16777216)",
}


SNOWFLAKE_TO_PYTHON: Dict[str, type] = {
    SnowflakeType.STRING: str,
    SnowflakeType.TEXT: str,
    SnowflakeType.VARCHAR: str,
    SnowflakeType.CHAR: str,
    SnowflakeType.NUMBER: Decimal,
    SnowflakeType.DECIMAL: Decimal,
    SnowflakeType.NUMERIC: Decimal,
    SnowflakeType.INTEGER: int,
    SnowflakeType.INT: int,
    SnowflakeType.BIGINT: int,
    SnowflakeType.SMALLINT: int,
    SnowflakeType.FLOAT: float,
    SnowflakeType.FLOAT8: float,
    SnowflakeType.DOUBLE: float,
    SnowflakeType.REAL: float,
    SnowflakeType.BOOLEAN: bool,
    SnowflakeType.BOOL: bool,
    SnowflakeType.DATE: date,
    SnowflakeType.DATETIME: datetime,
    SnowflakeType.TIMESTAMP: datetime,
    SnowflakeType.TIMESTAMP_LTZ: datetime,
    SnowflakeType.TIMESTAMP_NTZ: datetime,
    SnowflakeType.TIMESTAMP_TZ: datetime,
    SnowflakeType.TIME: time,
    SnowflakeType.BINARY: bytes,
    SnowflakeType.VARBINARY: bytes,
    SnowflakeType.BLOB: bytes,
    SnowflakeType.ARRAY: list,
    SnowflakeType.VARIANT: Any,
    SnowflakeType.OBJECT: dict,
}


def get_snowflake_type(
    python_type: type, precision: Optional[int] = None, scale: Optional[int] = None
) -> str:
    """Convert Python type to Snowflake type."""
    if python_type in PYTHON_TO_SNOWFLAKE:
        return PYTHON_TO_SNOWFLAKE[python_type]
    if python_type == float:
        return SnowflakeType.FLOAT
    if python_type == list:
        return SnowflakeType.ARRAY
    if python_type == dict:
        return SnowflakeType.OBJECT
    return SnowflakeType.VARCHAR(16777216)


def get_python_type(snowflake_type: str) -> type:
    """Convert Snowflake type to Python type."""
    base_type = snowflake_type.split("(")[0].strip()
    return SNOWFLAKE_TO_PYTHON.get(base_type, str)


class ColumnDefinition:
    """Represents a column definition for table creation."""

    def __init__(
        self,
        name: str,
        sql_type: str,
        nullable: bool = True,
        default: Optional[Any] = None,
        comment: Optional[str] = None,
    ):
        self.name = name
        self.sql_type = sql_type
        self.nullable = nullable
        self.default = default
        self.comment = comment

    def to_sql(self) -> str:
        parts = [f"{self.name} {self.sql_type}"]
        if not self.nullable:
            parts.append("NOT NULL")
        if self.default is not None:
            parts.append(f"DEFAULT {self._format_default()}")
        if self.comment:
            comment_escaped = self.comment.replace("'", "''")
            parts.append(f"COMMENT '{comment_escaped}'")
        return " ".join(parts)

    def _format_default(self) -> str:
        if isinstance(self.default, str):
            escaped = self.default.replace("'", "''")
            return f"'{escaped}'"
        if isinstance(self.default, (list, dict)):
            import json

            return f"'{json.dumps(self.default)}'"
        return str(self.default)

    def __repr__(self) -> str:
        return (
            f"ColumnDefinition({self.name}, {self.sql_type}, nullable={self.nullable})"
        )


class TableDefinition:
    """Represents a table definition for SQL generation."""

    def __init__(
        self,
        name: str,
        columns: List[ColumnDefinition],
        comment: Optional[str] = None,
    ):
        self.name = name
        self.columns = columns
        self.comment = comment

    def to_sql(self, primary_key: Optional[List[str]] = None) -> str:
        col_sql = ", ".join(col.to_sql() for col in self.columns)

        sql_parts = [f"CREATE TABLE IF NOT EXISTS {self.name} ({col_sql})"]

        if primary_key:
            pk_sql = ", ".join(primary_key)
            sql_parts.append(f"PRIMARY KEY ({pk_sql})")

        if self.comment:
            comment_escaped = self.comment.replace("'", "''")
            sql_parts.append(f"COMMENT '{comment_escaped}'")

        return " ".join(sql_parts)

    def __repr__(self) -> str:
        return f"TableDefinition({self.name}, {len(self.columns)} columns)"
