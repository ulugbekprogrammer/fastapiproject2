from sqlalchemy import create_engine, text
import database
from sqlalchemy.orm import sessionmaker
import main
from fastapi.testclient import TestClient
import pytest
from models import Todos

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

database.Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try: 
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'Ula', 'id': 1, 'user_role': 'admin'}

client = TestClient(main.app)

@pytest.fixture
def test_todo():
    todo = Todos (
        title="orange",
        description="blabla",
        priority=5,
        complete=False,
        owner_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()

    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()