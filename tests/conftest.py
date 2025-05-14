from sqlite3 import dbapi2
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base
from alembic import command

from app.main import app
from app import schemas
from app.config import settings
from app.oauth2 import create_access_token
from app import models
from app.database import get_db, Base, get_database_url


TEST_DATABASE_URL = get_database_url(testing=True)
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email":"hello123@gmail.com",
                  "password": "password123" }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email":"star@gmail.com",
                  "password": "password123" }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user



@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
    {
            "title": "title",
            "content": "content",
            "owner_id": test_user["id"]
         },
         {
             "title" : "2nd title",
             "content": "2nd content",
             "owner_id": test_user["id"]

         },
         {
             "title": "3rd title",
             "content": "3rd content",
             "owner_id": test_user["id"]
         },
         {
             "title": "4th title",
             "content": "4th content",
             "owner_id": test_user2["id"]
         }]
    
    posts = [models.Post(**post) for post in posts_data]
    
    session.add_all(posts)
    session.commit()

    stmt = select(models.Post)
    posts = session.execute(stmt).scalars().all()
    print(posts)
    return posts
    


