from database import Base, engine
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey



class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index= True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
    role = Column(String)

class Todos(Base):
    __tablename__ = 'todos'
    
    id  = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    
    
    

# # to Create database 
# Base.metadata.create_all(bind=engine)
