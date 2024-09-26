from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel  # data validation
from starlette import status
from sqlalchemy.orm import Session                      
from ..database import SessionLocal
from ..model import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# KEY GENERATED USING 'openssl rand -hex 32'
SECRET_KEY = 'd3da0056bb53a22276934f83c359c92abd9065bb9ba66cbc7f600a20b1faa9a5'
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
db_dependancy = Annotated[Session, Depends(get_db)]
template = Jinja2Templates(directory="TodoApp/templates")


### Pages ###

@router.get('/login-page')
def render_login_page(request:Request):
    return template.TemplateResponse("login.html",{"request":request})

@router.get('/register-page')
def render_register_page(request:Request):
    return template.TemplateResponse("register.html",{"request":request})


### EndPoints ###
class CreateRequestUser(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password:str
    role: str        

class Token(BaseModel):
    access_token:str
    token_type:str
    
    
async def get_current_user(token:Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=ALGORITHM)
        username:str = payload.get('sub')
        user_id:int = payload.get('id')
        user_role:str = payload.get('role')
        
        if username is None and user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        
        return  {"username":username,'user_id':user_id, "user_role":user_role}
             
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    

def authenticate_user(username:str, password:str, db):
    user = db.query(Users).filter(Users.username==username).first()
    if not user:
        return False
    
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
     
    return user


def create_access_token(username:str, user_id:int, role:str, expire_delta:timedelta):
    encode = {"sub":username,"id":user_id, "role":role}
    expires = datetime.now(timezone.utc) + expire_delta
    encode.update({'expire':expires.isoformat()})
    
    return jwt.encode(encode, SECRET_KEY,algorithm=ALGORITHM )
    
        
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependancy ,create_user_request:CreateRequestUser):
    user_model = Users(
        username = create_user_request.username, 
        email = create_user_request.email,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True,
        role = create_user_request.role
        )
    
    
    db.add(user_model)
    db.commit()
    
    
@router.post('/token', response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(db:db_dependancy, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
    
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    
    return {'access_token':token, 'token_type':'bearer'}
    
