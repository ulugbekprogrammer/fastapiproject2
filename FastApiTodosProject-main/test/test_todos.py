from sqlalchemy import create_engine
import database
from sqlalchemy.orm import sessionmaker
import main

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:ulugbek007@localhost:5432/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

database.Base.metadata.create_all(blind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try: 
        yield db
    finally:
        db.close()

main.app.dependency_overrides[database.get_db] = override_get_db