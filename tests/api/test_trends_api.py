import os
import uuid
import pytest
import psycopg
from psycopg.conninfo import conninfo_to_dict
from fastapi.testclient import TestClient
from backend.services.api.main import app

@pytest.fixture
def local_db_url(monkeypatch):
    """Point the API at the local test database for this test only."""
    url = os.environ.get("TEST_DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL is not set")
    host = conninfo_to_dict(url).get("host")
    is_local = host in ("localhost", "127.0.0.1") or (host or "").startswith("/")
    assert is_local, f"Refusing to run tests against {host}"
    monkeypatch.setenv("DATABASE_URL", url)   # get_connection() now uses the local DB
    return url

def test_trends_endpoint_counts_articles(local_db_url):
    client = TestClient(app)
    with psycopg.connect(local_db_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO aggregates_trend (source_type, source_name, title, link, published_at) "
                "VALUES ('test', 'test', 'test article', %s, NOW()) RETURNING id",
                (f"https://example.com/{uuid.uuid4()}",),
            )
            article_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO article_entities (article_id, entity_type, entity_value) "
                "VALUES (%s, 'trend', 'test trend xyz')",
                (article_id,),
            )
        conn.commit()
        try:
            response = client.get("/api/trends?entity_type=trend&time_window=30")
            assert response.status_code == 200 # status code is 200
            assert {"entity": "test trend xyz", "total": 1} in response.json()
        finally:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM aggregates_trend WHERE id = %s", (article_id,))
            conn.commit()