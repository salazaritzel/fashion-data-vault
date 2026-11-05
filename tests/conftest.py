import pytest
from backend.services.nlp.entity_extractor import EntityExtractor
import os
import psycopg
from psycopg.conninfo import conninfo_to_dict
from dotenv import load_dotenv

load_dotenv()
@pytest.fixture(scope = "module")
def extractor():
    return EntityExtractor()

@pytest.fixture
def conn():
    url = os.environ.get("TEST_DATABASE_URL")
    if not url:
        pytest.skip("TEST_DATABASE_URL is not set")
    host = conninfo_to_dict(url).get("host")
    is_local = host in ("localhost", "127.0.0.1") or (host or "").startswith("/")
    assert is_local, f"Refusing to run tests against {host}"
    connection = psycopg.connect(url)
    yield connection
    connection.close()