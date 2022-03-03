from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import Base
from ...main import app, getDb


# Database URL: SQL Lite 
# PostgreSQL: "postgresql://user:password@postgresserver/db"
# SQLite: "sqlite:///./sql_app.db"
dbUrl =  "sqlite:///./test.db"

# SQLALchemy engine 
engine = create_engine(
    dbUrl, connect_args={"check_same_thread": False} 
    # "check_same_thread": False
    # check_same_thread not needed for PostgreSQL
)

# Session 
testSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base: Returns class 
Base.metadata.create_all(bind=engine)

# Dependency
'''
- Independent database session/connection per request
- Use the same session through all the request
- Close session after all requests are completed 
'''

def overrideGetDb():
    try:
        db = testSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[getDb] = overrideGetDb

# App
client = TestClient(app)


def testCreateUser():
    # Create new user 
    response = client.post(
        "/user/",
        json={"email": "testEmail1@gmail.com", 
            "hashedPw": "testPw1", 
            "fName": "First", 
            "lName": "TestEmail",
            "contactNo": "87654321"},
    )

    assert response.status_code == 200, response.text

    data = response.json()
    assert data["email"] == "testEmail1@gmail.com"
    assert data["hashedPw"] == "testPw1"
    assert data["fName"] == "First"
    assert data["TestEmail"] == "TestEmail"
    assert data["contactNo"] == "87654321"

    assert "id" in data
    user_id = data["id"]

    # View new user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["email"] == "testEmail1@gmail.com"
    assert data["hashedPw"] == "testPw1"
    assert data["fName"] == "First"
    assert data["TestEmail"] == "TestEmail"
    assert data["contactNo"] == "87654321"

    assert data["id"] == user_id

def testCreateUserNoContactNo():
    # Create new user 
    response = client.post(
        "/user/",
        json={"email": "testEmail2@gmail.com", 
            "hashedPw": "testPw2", 
            "fName": "Second", 
            "lName": "TestEmail",
            "contactNo": ""},
    )

    assert response.status_code == 200, response.text

    data = response.json()
    assert data["email"] == "testEmail2@gmail.com"
    assert data["hashedPw"] == "testPw2"
    assert data["fName"] == "Second"
    assert data["TestEmail"] == "TestEmail"
    assert data["contactNo"] == ""

    assert "id" in data
    user_id = data["id"]

    # View new user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["email"] == "testEmail2@gmail.com"
    assert data["hashedPw"] == "testPw2"
    assert data["fName"] == "Second"
    assert data["TestEmail"] == "TestEmail"
    assert data["contactNo"] == ""

    assert data["id"] == user_id
