import os
import threading
from typing import Any, Dict, List, Optional

try:
    import snowflake.connector

    SNOWFLAKE_SQL_AVAILABLE = True
except ImportError:
    SNOWFLAKE_SQL_AVAILABLE = False

from ..exceptions import ConnectionError as WSnowflakeConnectionError


class ConnectionManager:
    """Manages Snowflake database connections with thread-local support."""

    _instance: Optional["ConnectionManager"] = None
    _lock = threading.Lock()

    def __init__(
        self,
        user: Optional[str] = None,
        password: Optional[str] = None,
        account: Optional[str] = None,
        warehouse: Optional[str] = None,
        database: Optional[str] = None,
        schema: Optional[str] = None,
        role: Optional[str] = None,
        login_timeout: int = 60,
        network_timeout: int = 30,
    ):
        self.user = user or os.environ.get("SNOWFLAKE_USER")
        self.password = password or os.environ.get("SNOWFLAKE_PASSWORD")
        self.account = account or os.environ.get("SNOWFLAKE_ACCOUNT")
        self.warehouse = warehouse or os.environ.get("SNOWFLAKE_WAREHOUSE")
        self.database = database or os.environ.get("SNOWFLAKE_DATABASE")
        self.schema = schema or os.environ.get("SNOWFLAKE_SCHEMA")
        self.role = role or os.environ.get("SNOWFLAKE_ROLE")
        self.login_timeout = login_timeout
        self.network_timeout = network_timeout

        if not self.user:
            raise WSnowflakeConnectionError("user is required")
        if not self.password:
            raise WSnowflakeConnectionError("password is required")
        if not self.account:
            raise WSnowflakeConnectionError("account is required")

        self._thread_local = threading.local()

    @classmethod
    def get_instance(
        cls,
        user: Optional[str] = None,
        password: Optional[str] = None,
        account: Optional[str] = None,
        warehouse: Optional[str] = None,
        database: Optional[str] = None,
        schema: Optional[str] = None,
        role: Optional[str] = None,
    ) -> "ConnectionManager":
        """Get or create a singleton ConnectionManager instance."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(
                    user=user,
                    password=password,
                    account=account,
                    warehouse=warehouse,
                    database=database,
                    schema=schema,
                    role=role,
                )
            return cls._instance

    @classmethod
    def reset_instance(cls) -> None:
        """Reset the singleton instance."""
        with cls._lock:
            if cls._instance:
                cls._instance.close()
            cls._instance = None

    def _create_connection_params(self) -> Dict[str, Any]:
        """Build connection parameters dictionary."""
        params = {
            "user": self.user,
            "password": self.password,
            "account": self.account,
            "login_timeout": self.login_timeout,
            "network_timeout": self.network_timeout,
        }
        if self.warehouse:
            params["warehouse"] = self.warehouse
        if self.database:
            params["database"] = self.database
        if self.schema:
            params["schema"] = self.schema
        if self.role:
            params["role"] = self.role
        return params

    def get_connection(self) -> Any:
        """Get a thread-local Snowflake connection."""
        if not SNOWFLAKE_SQL_AVAILABLE:
            raise WSnowflakeConnectionError(
                "snowflake-connector-python is not installed. "
                "Install with: pip install snowflake-connector-python"
            )

        if (
            not hasattr(self._thread_local, "connection")
            or self._thread_local.connection is None
        ):
            try:
                self._thread_local.connection = snowflake.connector.connect(
                    **self._create_connection_params()
                )
            except Exception as e:
                raise WSnowflakeConnectionError(f"Failed to connect to Snowflake: {e}")

        return self._thread_local.connection

    def get_cursor(self) -> Any:
        """Get a cursor from the current connection."""
        return self.get_connection().cursor()

    def close(self) -> None:
        """Close the thread-local connection."""
        if hasattr(self._thread_local, "connection") and self._thread_local.connection:
            try:
                self._thread_local.connection.close()
            except Exception:
                pass
            self._thread_local.connection = None

    def commit(self) -> None:
        """Commit the current transaction."""
        conn = self.get_connection()
        conn.commit()

    def rollback(self) -> None:
        """Rollback the current transaction."""
        conn = self.get_connection()
        conn.rollback()

    def ping(self) -> bool:
        """Ping the database to check connection health."""
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            return True
        except Exception:
            return False

    def list_warehouses(self) -> List[str]:
        """List available warehouses."""
        cursor = self.get_cursor()
        try:
            cursor.execute("SHOW WAREHOUSES")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        finally:
            cursor.close()

    def list_databases(self) -> List[str]:
        """List available databases."""
        cursor = self.get_cursor()
        try:
            cursor.execute("SHOW DATABASES")
            rows = cursor.fetchall()
            return [row[0] for row in rows]
        finally:
            cursor.close()

    def list_schemas(self, database: Optional[str] = None) -> List[str]:
        """List schemas in a database."""
        if database:
            cursor = self.get_cursor()
            try:
                cursor.execute(f"SHOW SCHEMAS IN {database}")
                rows = cursor.fetchall()
                return [row[0] for row in rows]
            finally:
                cursor.close()
        return []

    def get_current_warehouse(self) -> Optional[str]:
        """Get the current warehouse."""
        cursor = self.get_cursor()
        try:
            cursor.execute("SELECT CURRENT_WAREHOUSE()")
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            cursor.close()

    def get_current_database(self) -> Optional[str]:
        """Get the current database."""
        cursor = self.get_cursor()
        try:
            cursor.execute("SELECT CURRENT_DATABASE()")
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            cursor.close()

    def get_current_schema(self) -> Optional[str]:
        """Get the current schema."""
        cursor = self.get_cursor()
        try:
            cursor.execute("SELECT CURRENT_SCHEMA()")
            result = cursor.fetchone()
            return result[0] if result else None
        finally:
            cursor.close()
