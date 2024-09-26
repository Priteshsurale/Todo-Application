from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_user(test_users):
    response = client.get('/user/')
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'priteshsurale'
    assert response.json()['first_name'] == 'pritesh'
    assert response.json()['last_name'] == 'surale' 
    
    
def test_change_password_success(test_users):
    response = client.put('/user/password',json={'password':'pass@1234', 'new_password':'newpassword'})
        
    assert response.status_code == 204


def test_change_password_invalid_current_password(test_users):
    response = client.put('/user/password',json={'password':'new_password', 'new_password':'newpassword'})
    
    
    assert response.status_code == 401
    assert response.json() == {"detail":'Old Password Dosen\'t Matched'}