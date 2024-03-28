from unittest.mock import MagicMock, patch
import pytest

from app.db.base_queries import BaseQueries


@pytest.fixture
def base_queries():
    return BaseQueries()    


@pytest.mark.asyncio
async def test_base_queries_get_all(base_queries):
    with patch("app.db.base_queries.connect_db") as mock_connect_db:
        mock_cursor = MagicMock()
        mock_connect_db.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [{"id": 1, "name": "test"}]
        result = await base_queries.get_all()
        assert result == [{"id": 1, "name": "test"}]