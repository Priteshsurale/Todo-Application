from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from ..model import Todos
from ..database import SessionLocal
from .auth import get_current_user

router = APIRouter()

def get_db():
    db =  SessionLocal()
    try:
        yield db
        
    finally:
        db.close()
        
    
# PYDANTIC CLASS
class TodoRequest(BaseModel):
    title : str = Field(min_length=3)
    description : str = Field(min_length=3, max_length=100)
    priority : int = Field(gt=0,lt=6)
    complete : bool


# Annotated in python allows developers to declare the type of a reference and provide additional information related to it. 
# Depends: the mechanism where an object receives other objects that it depends on. The other objects are called dependencies.
db_dependancy = Annotated[Session, Depends(get_db)] 
user_dependancy = Annotated[dict, Depends(get_current_user)]

# GET ALL TODOS
@router.get('/', status_code=status.HTTP_200_OK)
async def read_all(user:user_dependancy,db:db_dependancy):
    if user is None:
        raise HTTPException(status=401, detail='Authentication Failed')

    return db.query(Todos).filter(Todos.owner_id == user.get('user_id')).all()
    

# GET TODOS BY ID
@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def get_todo(user:user_dependancy, db:db_dependancy, todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('user_id')).first()
    if todo_model is not None:
        return todo_model
    
    raise HTTPException(status_code=404, detail='Todo Not Found')


# ADD TODOS
@router.post('/todo',status_code=status.HTTP_201_CREATED)
async def add_todo(user:user_dependancy, db:db_dependancy, todo_data:TodoRequest):
    
    if user is None:
        return HTTPException(status_code=401, detail='Authentication Failed')
    

    todo_model = Todos(**todo_data.model_dump(),owner_id=user.get('user_id'))
    db.add(todo_model)
    db.commit()
    

# UPDATE TODOS
@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user:user_dependancy, db:db_dependancy, todo_data:TodoRequest, todo_id:int=Path(gt=0)):
    if user is None:
        return HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('user_id')).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    
    todo_model.title = todo_data.title
    todo_model.description = todo_data.description
    todo_model.priority = todo_data.priority
    todo_model.complete = todo_data.complete
    
    db.add(todo_model)
    db.commit()
    
 
# DELETE TODOS 
@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependancy ,db:db_dependancy, todo_id:int=Path(gt=0)):
    if user is None:
        return HTTPException(status_code=401, detail='Authentication Failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('user_id')).first()
    
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo Not Found")
    
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('user_id')).delete()
    db.commit()
    
    
