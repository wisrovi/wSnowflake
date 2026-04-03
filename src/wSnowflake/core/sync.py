from typing import Any, Dict, List, Optional

from ..exceptions import TableSyncError
from ..types.sql_types import ColumnDefinition, TableDefinition
from .connection import ConnectionManager


class TableSync:
    """Manages Snowflake table schema synchronization."""

    def __init__(self, connection_manager: Optional[ConnectionManager] = None):
        self._cm = connection_manager or ConnectionManager.get_instance()

    def create_table_if_not_exists(
        self,
        table_name: str,
        columns: List[ColumnDefinition],
        primary_key: Optional[List[str]] = None,
        comment: Optional[str] = None,
    ) -> bool:
        """Create a table if it doesn't exist."""
        if self.table_exists(table_name):
            return False

        table_def = TableDefinition(
            name=table_name,
            columns=columns,
            comment=comment,
        )
        query = table_def.to_sql(primary_key=primary_key)
        cursor = self._cm.get_cursor()
        try:
            cursor.execute(query)
            self._cm.commit()
            return True
        except Exception as e:
            self._cm.rollback()
            raise TableSyncError(f"Failed to create table {table_name}: {e}")
        finally:
            cursor.close()

    def add_column(self, table_name: str, column: ColumnDefinition) -> bool:
        """Add a column to an existing table."""
        if not self.column_exists(table_name, column.name):
            cursor = self._cm.get_cursor()
            try:
                query = f"ALTER TABLE {table_name} ADD COLUMN {column.to_sql()}"
                cursor.execute(query)
                self._cm.commit()
                return True
            except Exception as e:
                self._cm.rollback()
                raise TableSyncError(
                    f"Failed to add column {column.name} to {table_name}: {e}"
                )
            finally:
                cursor.close()
        return False

    def add_columns(
        self, table_name: str, columns: List[ColumnDefinition]
    ) -> List[str]:
        """Add multiple columns to an existing table."""
        added = []
        for column in columns:
            if self.add_column(table_name, column):
                added.append(column.name)
        return added

    def alter_column(
        self,
        table_name: str,
        column_name: str,
        new_type: Optional[str] = None,
        new_nullable: Optional[bool] = None,
        new_default: Optional[Any] = None,
    ) -> bool:
        """Alter a column's properties."""
        alterations = []
        if new_type:
            alterations.append(
                f"ALTER TABLE {table_name} ALTER COLUMN {column_name} SET DATA TYPE {new_type}"
            )
        if new_nullable is not None:
            if new_nullable:
                alterations.append(
                    f"ALTER TABLE {table_name} ALTER COLUMN {column_name} DROP NOT NULL"
                )
            else:
                alterations.append(
                    f"ALTER TABLE {table_name} ALTER COLUMN {column_name} SET NOT NULL"
                )
        if new_default is not None:
            alterations.append(
                f"ALTER TABLE {table_name} ALTER COLUMN {column_name} SET DEFAULT {new_default}"
            )

        if not alterations:
            return False

        cursor = self._cm.get_cursor()
        try:
            for query in alterations:
                cursor.execute(query)
            self._cm.commit()
            return True
        except Exception as e:
            self._cm.rollback()
            raise TableSyncError(f"Failed to alter column {column_name}: {e}")
        finally:
            cursor.close()

    def drop_column(self, table_name: str, column_name: str) -> bool:
        """Drop a column from a table."""
        cursor = self._cm.get_cursor()
        try:
            query = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
            cursor.execute(query)
            self._cm.commit()
            return True
        except Exception as e:
            self._cm.rollback()
            raise TableSyncError(f"Failed to drop column {column_name}: {e}")
        finally:
            cursor.close()

    def rename_column(self, table_name: str, old_name: str, new_name: str) -> bool:
        """Rename a column."""
        cursor = self._cm.get_cursor()
        try:
            query = f"ALTER TABLE {table_name} RENAME COLUMN {old_name} TO {new_name}"
            cursor.execute(query)
            self._cm.commit()
            return True
        except Exception as e:
            self._cm.rollback()
            raise TableSyncError(f"Failed to rename column {old_name}: {e}")
        finally:
            cursor.close()

    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists."""
        cursor = self._cm.get_cursor()
        try:
            cursor.execute(f"DESCRIBE TABLE {table_name}")
            return True
        except Exception:
            return False
        finally:
            cursor.close()

    def column_exists(self, table_name: str, column_name: str) -> bool:
        """Check if a column exists in a table."""
        cursor = self._cm.get_cursor()
        try:
            cursor.execute(f"DESCRIBE TABLE {table_name}")
            rows = cursor.fetchall()
            columns_desc = [desc[0] for desc in cursor.description]
            for row in rows:
                row_dict = dict(zip(columns_desc, row))
                if row_dict.get("name", "").lower() == column_name.lower():
                    return True
            return False
        finally:
            cursor.close()

    def get_table_columns(self, table_name: str) -> List[Dict[str, Any]]:
        """Get all columns of a table."""
        cursor = self._cm.get_cursor()
        try:
            cursor.execute(f"DESCRIBE TABLE {table_name}")
            rows = cursor.fetchall()
            columns_desc = [desc[0] for desc in cursor.description]
            return [dict(zip(columns_desc, row)) for row in rows]
        finally:
            cursor.close()

    def sync_columns(
        self,
        table_name: str,
        columns: List[ColumnDefinition],
    ) -> Dict[str, Any]:
        """Synchronize table columns - add missing columns."""
        if not self.table_exists(table_name):
            raise TableSyncError(f"Table {table_name} does not exist")

        existing_columns = self.get_table_columns(table_name)
        existing_names = {col["name"].lower() for col in existing_columns}

        added = []
        for col in columns:
            if col.name.lower() not in existing_names:
                self.add_column(table_name, col)
                added.append(col.name)

        return {"added": added}

    def add_comment(
        self,
        table_name: Optional[str] = None,
        column_name: Optional[str] = None,
        comment: str = "",
    ) -> bool:
        """Add comment to a table or column."""
        if table_name and column_name:
            query = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} COMMENT '{comment}'"
        elif table_name:
            query = f"ALTER TABLE {table_name} COMMENT '{comment}'"
        else:
            raise TableSyncError(
                "Either table_name or both table_name and column_name required"
            )

        cursor = self._cm.get_cursor()
        try:
            cursor.execute(query)
            self._cm.commit()
            return True
        except Exception as e:
            self._cm.rollback()
            raise TableSyncError(f"Failed to add comment: {e}")
        finally:
            cursor.close()

    def add_primary_key(self, table_name: str, columns: List[str]) -> bool:
        """Add a primary key to a table."""
        cursor = self._cm.get_cursor()
        try:
            columns_str = ", ".join(columns)
            query = f"ALTER TABLE {table_name} ADD PRIMARY KEY ({columns_str})"
            cursor.execute(query)
            self._cm.commit()
            return True
        except Exception as e:
            self._cm.rollback()
            raise TableSyncError(f"Failed to add primary key: {e}")
        finally:
            cursor.close()
