import pytest


class TestWSnowflakeImport:
    def test_import(self):
        from wSnowflake import WSnowflake
        assert WSnowflake is not None

    def test_version(self):
        import wSnowflake
        assert wSnowflake.__version__ == "1.0.0"


class TestQueryBuilder:
    def test_import(self):
        from wSnowflake import QueryBuilder
        qb = QueryBuilder()
        assert qb is not None


class TestExceptions:
    def test_import(self):
        from wSnowflake import WSnowflakeError
        with pytest.raises(WSnowflakeError):
            raise WSnowflakeError("test")