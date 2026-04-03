"""
Comprehensive test suite for wSnowflake library.
"""

import pytest


class TestWSnowflakeImport:
    """Test basic imports."""

    def test_import_main_class(self):
        from wSnowflake import WSnowflake
        assert WSnowflake is not None

    def test_import_connection_manager(self):
        from wSnowflake import ConnectionManager
        assert ConnectionManager is not None

    def test_import_query_builder(self):
        from wSnowflake import QueryBuilder
        assert QueryBuilder is not None

    def test_version(self):
        import wSnowflake
        assert wSnowflake.__version__ == "1.0.0"


class TestExceptions:
    """Test exception hierarchy."""

    def test_wsnowflake_error(self):
        from wSnowflake import WSnowflakeError
        with pytest.raises(WSnowflakeError):
            raise WSnowflakeError("test")

    def test_connection_error(self):
        from wSnowflake import ConnectionError
        with pytest.raises(ConnectionError):
            raise ConnectionError("test")

    def test_query_error(self):
        from wSnowflake import QueryError
        with pytest.raises(QueryError):
            raise QueryError("test")

    def test_validation_error(self):
        from wSnowflake import ValidationError
        with pytest.raises(ValidationError):
            raise ValidationError("test")

    def test_hierarchy(self):
        from wSnowflake import WSnowflakeError, ConnectionError
        assert issubclass(ConnectionError, WSnowflakeError)


class TestQueryBuilder:
    """Test QueryBuilder."""

    def test_fluent_api(self):
        from wSnowflake import QueryBuilder
        qb = QueryBuilder().select("*").from_table("users")
        assert qb is not None

    def test_where(self):
        from wSnowflake import QueryBuilder
        qb = QueryBuilder().select("*").from_table("users").where("id", "=", 1)
        query, _ = qb.build_select()
        assert "WHERE" in query

    def test_order_by(self):
        from wSnowflake import QueryBuilder
        qb = QueryBuilder().select("*").from_table("users").order_by("name")
        query, _ = qb.build_select()
        assert "ORDER BY name" in query

    def test_limit_offset(self):
        from wSnowflake import QueryBuilder
        qb = QueryBuilder().select("*").from_table("users").limit(10).offset(20)
        query, _ = qb.build_select()
        assert "LIMIT 10" in query
        assert "OFFSET 20" in query


class TestConnectionManager:
    """Test ConnectionManager."""

    def test_init(self):
        from wSnowflake import ConnectionManager
        cm = ConnectionManager(
            account="test_account",
            user="test_user",
            password="test_password",
            database="test_db"
        )
        assert cm is not None

    def test_thread_local(self):
        from wSnowflake import ConnectionManager
        cm = ConnectionManager(
            account="test_account",
            user="test_user",
            password="test_password"
        )
        assert hasattr(cm, '_thread_local')


class TestSqlTypes:
    """Test SQL type mapping."""

    def test_varchar_type(self):
        from wSnowflake.types import get_sql_type
        from pydantic import BaseModel

        class TestModel(BaseModel):
            name: str

        sql_type = get_sql_type(TestModel.model_fields["name"])
        assert "VARCHAR" in sql_type

    def test_integer_type(self):
        from wSnowflake.types import get_sql_type
        from pydantic import BaseModel

        class TestModel(BaseModel):
            id: int

        sql_type = get_sql_type(TestModel.model_fields["id"])
        assert "NUMBER" in sql_type or "INT" in sql_type

    def test_boolean_type(self):
        from wSnowflake.types import get_sql_type
        from pydantic import BaseModel

        class TestModel(BaseModel):
            active: bool

        sql_type = get_sql_type(TestModel.model_fields["active"])
        assert "BOOLEAN" in sql_type

    def test_timestamp_type(self):
        from wSnowflake.types import get_sql_type
        from datetime import datetime
        from pydantic import BaseModel

        class TestModel(BaseModel):
            created_at: datetime

        sql_type = get_sql_type(TestModel.model_fields["created_at"])
        assert "TIMESTAMP" in sql_type