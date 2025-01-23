import pytest
from sqlmodel import Session, SQLModel, create_engine
from fastapi.testclient import TestClient
from faker import Faker
from ..database import get_session, create_db_and_tables
from ..main import app

# Set up the test database   
DATABASE_URL = "sqlite:///./test.db"
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

def test_register_user(faker: Faker):
    response = client.post(
        "/user/register",
        json={
            "name": faker.first_name(),
            "surname": faker.last_name(),
            "email": faker.email(),
            "phone": faker.phone_number(),
            "password": faker.password()
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_user(faker: Faker):
    email = faker.email()
    password = faker.password()
    client.post(
        "/user/register",
        json={
            "name": faker.first_name(),
            "surname": faker.last_name(),
            "email": email,
            "phone": faker.phone_number(),
            "password": password
        }
    )
    response = client.post(
        "/user/token",
        json={
            "email": email,
            "password": password
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_get_current_user(faker: Faker):
    email = faker.email()
    password = faker.password()
    client.post(
        "/user/register",
        json={
            "name": faker.first_name(),
            "surname": faker.last_name(),
            "email": email,
            "phone": faker.phone_number(),
            "password": password
        }
    )
    login_response = client.post(
        "/user/token",
        json={
            "email": email,
            "password": password
        }
    )
    token = login_response.json()["access_token"]
    response = client.get(
        "/user/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == email