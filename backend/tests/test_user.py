import os
import pytest
from fastapi.testclient import TestClient
from backend.database import get_session, create_db_and_tables
from backend.main import app
from sqlmodel import Session, SQLModel, create_engine

# Set up the test database   
DATABASE_URL = "changeit!!"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Override the get_session dependency to use the test database
def override_get_session():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    SQLModel.metadata.create_all(engine)
    create_db_and_tables()
    yield
    SQLModel.metadata.drop_all(engine)

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/user/register",
        json={
            "name": "changeit!!",
            "surname": "changeit!!",
            "email": "changeit!!",
            "phone": "changeit!!",
            "password": "changeit!!"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_user():
    response = client.post(
        "/user/token",
        json={
            "email": "changeit!!",
            "password": "changeit!!"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_current_user():
    login_response = client.post(
        "/user/token",
        json={
            "email": "changeit!!",
            "password": "changeit!!"
        }
    )
    token = login_response.json()["access_token"]
    response = client.get(
        "/user/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "changeit!!"


# Check this code this I assume I've done smth wrong