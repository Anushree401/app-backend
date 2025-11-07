import io
import csv
import pytest
from fastapi.testclient import TestClient
from app.main import app
from models.database import Base, UserDB
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ---------- SETUP ----------

SQLALCHEMY_TEST_URL = "sqlite:///./test_credit_history.db"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.fixture(scope="function")
def db_session():
    """Creates a fresh database for each test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()


# ---------- HELPER ----------

def create_user(client, first_name="John", last_name="Doe", email="john@example.com"):
    response = client.post(
        "/user/add",
        json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone_number": "9876543210",
        },
    )
    assert response.status_code == 200
    return response.json()["user"]["unique_id"]


# ---------- TESTS ----------

def test_add_credit_history_entry(db_session, monkeypatch):
    """Ensure credit history entry can be created and fetched."""
    user_id = create_user(client)

    # Mock DB session injection
    monkeypatch.setattr("controllers.credit_history_controller.get_db", lambda: db_session)

    # Add credit history record
    response = client.post(
        f"/credit-history/add",
        json={
            "user_id": user_id,
            "transaction_type": "add",
            "amount": 50,
            "action_user": "admin",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Credit history added successfully"

    # Fetch the credit history
    res = client.get(f"/credit-history/{user_id}")
    assert res.status_code == 200
    history = res.json()["history"]
    assert len(history) == 1
    assert history[0]["points"] == 50
    assert history[0]["type"] == "add"


def test_credit_history_export_csv(db_session, monkeypatch):
    """Ensure CSV export route returns proper CSV file."""
    user_id = create_user(client)

    # Add a sample credit history entry
    client.post(
        f"/credit-history/add",
        json={
            "user_id": user_id,
            "transaction_type": "add",
            "amount": 100,
            "action_user": "admin",
        },
    )

    # Request CSV export
    res = client.get("/credit-history/export")
    assert res.status_code == 200
    assert res.headers["content-type"] == "text/csv; charset=utf-8"

    # Validate CSV content
    csv_content = res.content.decode("utf-8")
    reader = csv.reader(io.StringIO(csv_content))
    headers = next(reader)
    assert "user_id" in headers
    assert "points" in headers

    rows = list(reader)
    assert len(rows) >= 1
