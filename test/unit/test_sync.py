import pytest
from pydantic import BaseModel
from wSnowflake.core.sync import TableSync


class TestTableSync:
    def test_import(self):
        from wSnowflake.core.sync import TableSync

        assert TableSync is not None

    def test_sync_creation(self):
        from wSnowflake.core.sync import TableSync

        class User(BaseModel):
            id: int
            name: str

        sync = TableSync(User, {})
        assert sync.model == User
