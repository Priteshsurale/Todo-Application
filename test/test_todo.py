
from fastapi import status
from ..main import app
from ..model import Todos
from ..routers.todos import get_current_user, get_db
from .utils import *

        
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authentication(test_todo):
    response = client.get('/todos/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"complete":False,"title":'Learn To Code',"description":'Need to learn everyday!','id':1,"priority":5,'owner_id':1}]
    

def test_read_one_authentication(test_todo):
    response = client.get('/todos/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"complete":False,"title":'Learn To Code',"description":'Need to learn everyday!','id':1,"priority":5,'owner_id':1}
    


def test_read_one_authentication_not_found():
    response = client.get('/todos/todo/99')
    assert response.status_code == 404
    assert response.json() == {"detail":"Todo Not Found"}
    


def test_create_todo(test_todo):
    requested_data = {
        'title':'New todo!',
        'description':'New todo description',
        'priority':5,
        'complete':False,
    }
    
    response = client.post('/todos/todo/',json=requested_data)
    assert response.status_code == 201
    
    db = TestingSessionLocal()
    model_data = db.query(Todos).filter(Todos.id == 2).first()
    assert model_data.title == requested_data.get('title')
    assert model_data.description == requested_data.get('description')
    assert model_data.priority == requested_data.get('priority')
    assert model_data.complete == requested_data.get('complete')
    
    
def test_update_todo(test_todo):
    requested_data = {
        'title':'Change the title of the todo already saved!',
        'description':'Need to learn everyday!',
        'priority':5,
        'complete':False,
    }
    
    response = client.put('/todos/todo/1',json=requested_data)
    assert response.status_code == 204
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()

    assert model.title == requested_data.get('title')
    assert model.description == requested_data.get('description')
    assert model.priority == requested_data.get('priority')
    assert model.complete == requested_data.get('complete')
    
    
    
def test_update_todo_not_found():
    requested_data = {
        'title':'Change the title of the todo already saved!',
        'description':'Need to learn everyday!',
        'priority':5,
        'complete':False,
    }
    
    response = client.put('/todos/todo/99',json=requested_data)
    assert response.status_code == 404
    assert response.json() == {"detail":"Todo Not Found"}
    
    
def test_delete_todo(test_todo):
    response = client.delete('/todos/todo/1')
    assert response.status_code == 204
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id==1).first()
    
    assert model is None
    
    
def test_delete_todo_not_found():
    response = client.delete('/todos/todo/99')
    
    assert response.status_code == 404
    assert response.json() == {"detail":"Todo Not Found"}
    
    