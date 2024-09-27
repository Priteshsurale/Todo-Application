from fastapi import APIRouter, Depends, HTTPException, Path
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from starlette import status
from typing import Annotated
from sqlalchemy.orm import Session
from ..model import Users
from ..database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix='/user',
    tags=['user']
)

def get_db():
    db =  SessionLocal()
    try:
        yield db
        
    finally:
        db.close()
        

# Annotated in python allows developers to declare the type of a reference and provide additional information related to it. 
# Depends: the mechanism where an object receives other objects that it depends on. The other objects are called dependencies.
db_dependancy = Annotated[Session, Depends(get_db)] 
user_dependancy = Annotated[dict, Depends(get_current_user)]
bcrypt = CryptContext(schemes=['bcrypt'], deprecated='auto')

"""
get_user: this endpoint should return all information about the user that is currently logged in.

change_password: this endpoint should allow a user to change their current password.
"""

class UserVerification(BaseModel):
    password: str 
    new_password:str = Field(min_length=6)
    
    
@router.get('/', status_code=status.HTTP_200_OK)
async def get_users(user: user_dependancy, db:db_dependancy):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    return db.query(Users).filter(Users.id == user.get('user_id')).first()



@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependancy, db:db_dependancy, user_data:UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    user_model = db.query(Users).filter(Users.id == user.get('user_id')).first()
    
    if not bcrypt.verify(user_data.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Old Password Dosen\'t Matched') 
    
    user_model.hashed_password = bcrypt.hash(user_data.new_password)
    
    db.add(user_model)
    db.commit()
    
    