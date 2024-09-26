from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..model import Todos, Users
import pytest
from ..main import app
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_ENGINE = 'sqlite:///./test.db'
engine = create_engine(SQLALCHEMY_DATABASE_ENGINE,
                       connect_args={'check_same_thread':False},
                       poolclass = StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
 
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username':'priteshsurale','user_id':1,'user_role':'admin'}


client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title='Learn To Code',
        description='Need to learn everyday!',
        priority=5,
        complete=False,
        owner_id=1,
    )
    
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM TODOS;"))
        connection.commit()


@pytest.fixture
def test_users():
    user = Users(
        username='priteshsurale',
        email='priteshsurale@gmail.com',
        first_name='pritesh',
        last_name='surale',
        hashed_password= bcrypt_context.hash('pass@1234'),
        role='admin',
        is_active=True
    )
    
    db = TestingSessionLocal()
    
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM USERS;'))
        connection.commit()
        