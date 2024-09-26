from .utils import *
from ..routers.auth import authenticate_user, get_current_user, get_db, create_access_token, SECRET_KEY, ALGORITHM
from jose import jwt
from datetime import timedelta
import pytest
from fastapi import HTTPException

app.dependency_overrides[get_db] = override_get_db
 
 

def test_authenticate_user(test_users):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_users.username,'pass@1234',db)
    
    assert authenticated_user is not None
    assert authenticated_user.username == test_users.username
    
    
    non_existent_user = authenticate_user('testUsername', 'dead', db)
    assert non_existent_user is False
    
    wrong_password_user = authenticate_user('priteshsurale', 'dead', db)
    assert wrong_password_user is False
    

def test_create_access_token():
    username = 'priteshsurale'
    user_id = 1
    role = 'user'
    expire = timedelta(days=1)
    
    token = create_access_token(username, user_id, role, expire)
    
    decode = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM,options={'verify_signature':False})
    
    assert decode['sub'] ==  username
    assert decode['id'] == user_id
    assert decode['role'] == role
    

@pytest.mark.asyncio
async def test_get_current_user_valid_token():
    encode = {'sub':'testuser', 'id':1, 'role':'admin'}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    
    
    user = await get_current_user(token)

    assert user == {"username":'testuser','user_id':1, "user_role":'admin'}
    


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    encode = {'role':'user'}
    
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)
        
    assert excinfo.value.status_code  == 401
    assert excinfo.value.detail  == "Could not validate user"
    
    