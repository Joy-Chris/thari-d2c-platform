import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import db

@pytest.fixture(scope="session")
def client():
    """
    FastAPI test client fixture.
    """
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(autouse=True)
def reset_db_state():
    """
    Reload seed data before each test to ensure test isolation.
    """
    db.load_seed_data()
    yield
