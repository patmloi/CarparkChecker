from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database import Base
from db import crud
from main import app, getDb, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

from passlib.context import CryptContext

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

from jose import jwt
from datetime import datetime

import os
import pytest

testDbFile = "tests/test.db"
if os.path.isfile(testDbFile):
    os.remove(testDbFile)

# Database URL: SQL Lite
# PostgreSQL: "postgresql://user:password@postgresserver/db"
# SQLite: "sqlite:///./sql_app.db"
dbUrl = f"sqlite:///./{testDbFile}"

# SQLALchemy engine
engine = create_engine(
    dbUrl,
    connect_args={"check_same_thread": False}
    # "check_same_thread": False
    # check_same_thread not needed for PostgreSQL
)

# Session
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: Returns class
Base.metadata.create_all(bind=engine)

# Dependency
"""
- Independent database session/connection per request
- Use the same session through all the request
- Close session after all requests are completed 
"""


def overrideGetDb():
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[getDb] = overrideGetDb

client = TestClient(app)


def createUser():
    # Create new user

    test_user_data = {
        "email": "testEmail1@gmail.com",
        "password": "testPw1123456",
        "fName": "First",
        "lName": "Last",
        "contactNo": "87654321",
    }

    response = client.post(
        "/register",
        json=test_user_data,
    )
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["fName"] == test_user_data["fName"]
    assert data["lName"] == test_user_data["lName"]
    assert data["contactNo"] == test_user_data["contactNo"]
    assert "password" not in data

    assert "id" in data
    userId = data["id"]

    for db_internal in overrideGetDb():
        user = crud.getUserById(db_internal, userId)
        assert user.email == test_user_data["email"]
        assert user.fName == test_user_data["fName"]
        assert user.lName == test_user_data["lName"]
        assert user.contactNo == test_user_data["contactNo"]
        assert pwdContext.verify(test_user_data["password"], user.hashedPw)

    return test_user_data


def createUserNoContactNo():
    # Create new user
    test_user_data = {
        "email": "testEmail2@gmail.com",
        "password": "testPw2123456",
        "fName": "Second",
        "lName": "Last",
        "contactNo": "",
    }

    response = client.post(
        "/register",
        json=test_user_data,
    )
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["fName"] == test_user_data["fName"]
    assert data["lName"] == test_user_data["lName"]
    assert data["contactNo"] == test_user_data["contactNo"]
    assert "password" not in data

    assert "id" in data
    userId = data["id"]

    for db_internal in overrideGetDb():
        user = crud.getUserById(db_internal, userId)
        assert user.email == test_user_data["email"]
        assert user.fName == test_user_data["fName"]
        assert user.lName == test_user_data["lName"]
        assert user.contactNo == test_user_data["contactNo"]
        assert pwdContext.verify(test_user_data["password"], user.hashedPw)

    return test_user_data


@pytest.fixture(scope="module")
def createTestDatabase():
    user1 = createUser()
    user2 = createUserNoContactNo()
    return (user1, user2)


@pytest.fixture(scope="module")
def getAuthenticatedToken(createTestDatabase):
    return test_loginSuccess(createTestDatabase)


def test_loginSuccess(createTestDatabase):

    user1, _ = createTestDatabase

    login_data = {"username": user1["email"], "password": user1["password"]}

    response = client.post("/token", data=login_data)
    assert response.status_code == 200, response.text

    data = response.json()
    assert "access_token" in data
    assert "token_type" in data

    access_token = data["access_token"]
    token_type = data["token_type"]

    assert token_type == "bearer"
    token_decoded = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])

    assert "id" in token_decoded
    assert "exp" in token_decoded

    now = datetime.now().timestamp()
    assert 0 <= ACCESS_TOKEN_EXPIRE_MINUTES * 60 - token_decoded["exp"] + now <= 60

    return access_token


def test_loginWrongPassword(createTestDatabase):

    user1, _ = createTestDatabase

    login_data = {"username": user1["email"], "password": "xxxx"}

    response = client.post("/token", data=login_data)
    assert response.status_code == 401, response.text

    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Incorrect username or password"


def test_loginWrongEmail(createTestDatabase):

    user1, _ = createTestDatabase

    login_data = {"username": "xxxx", "password": user1["password"]}

    response = client.post("/token", data=login_data)
    assert response.status_code == 404, response.text

    data = response.json()
    assert "detail" in data
    assert data["detail"] == "User not found"


def test_readMeAuthenticated(createTestDatabase, getAuthenticatedToken):

    user1, _ = createTestDatabase

    token = getAuthenticatedToken

    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["email"] == user1["email"]
    assert data["fName"] == user1["fName"]
    assert data["lName"] == user1["lName"]
    assert data["contactNo"] == user1["contactNo"]


def test_readMeUnauthenticated(createTestDatabase, getAuthenticatedToken):

    response = client.get(
        "/me",
    )
    assert response.status_code == 401, response.text

    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Not authenticated"


def test_readMeWrongToken(createTestDatabase, getAuthenticatedToken):

    token = getAuthenticatedToken
    invalid_token = token[:-5] + "eeeee"

    response = client.get("/me", headers={"Authorization": f"Bearer {invalid_token}"})

    assert response.status_code == 401, response.text

    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Could not validate credentials"


def test_availabilityAuthenticated(createTestDatabase, getAuthenticatedToken):

    token = getAuthenticatedToken
    response = client.post(
        "/availability",
        headers={"Authorization": f"Bearer {token}"},
        data={"dateTime": "2022-03-04 21:15:32.437896"},
    )
    assert response.status_code == 200

    data = response.json()
    assert "items" in data

    token = getAuthenticatedToken
    response = client.post(
        "/availability",
        headers={"Authorization": f"Bearer {token}"},
        data={"dateTime": ""},
    )
    assert response.status_code == 200

    data = response.json()
    assert "items" in data


def test_availabilityUnauthenticated(createTestDatabase, getAuthenticatedToken):

    token = getAuthenticatedToken
    response = client.post("/availability", data={"dateTime": ""})
    assert response.status_code == 401, response.text

    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Not authenticated"


def test_readMeWrongToken(createTestDatabase, getAuthenticatedToken):

    token = getAuthenticatedToken
    invalid_token = token[:-5] + "eeeee"

    response = client.get("/me", headers={"Authorization": f"Bearer {invalid_token}"})

    assert response.status_code == 401, response.text

    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Could not validate credentials"
