from sqlalchemy import create_engine, StaticPool, text
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..models import Todos, Users
import pytest
from ..main import app
from ..routers.auth import bcrypt_context
from fastapi.testclient import TestClient


SQLALCHAMY_DATABASE_URL = "sqlite:///./testdb.db"
engine = create_engine(
    SQLALCHAMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db

    finally:
        db.close()

def override_get_current_user():
    return {'username': 'codewithzubu', 'id': 1, 'user_role': 'admin'}


client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        id=1,
        title='Learn to code!',
        description='Need to learn everyday!',
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM TODOS;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="codewithzubu",
        first_name="Zubu",
        last_name="Abb",
        email="zubu@gmail.com",
        hashed_password=bcrypt_context.hash("Zubu@1234"),
        role="admin",
        phone_number="8888888888"
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM USERS;"))
        connection.commit()