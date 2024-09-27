from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from typing import Annotated
from sqlalchemy.orm import Session
from model import Todos
from database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['admin']
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



@router.get('/todo',status_code=status.HTTP_200_OK)
async def read_all(user: user_dependancy, db:db_dependancy):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    return db.query(Todos).all()


@router.delete('/todo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependancy, db:db_dependancy, todo_id:int=Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo Not Found.')
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit() 