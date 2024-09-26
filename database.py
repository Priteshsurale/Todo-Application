from sqlalchemy import create_engine                        # creates a new SQLAlchemy Engine object
from sqlalchemy.orm import sessionmaker, declarative_base  

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# engine = create_engine(POSTGRES_DATABASE_URL, connect_args={'check_same_thread':False})

POSTGRES_DATABASE_URL = 'postgresql://priteshs:password@localhost/TodoApplication'

engine = create_engine(POSTGRES_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # the sessionmaker class is normally used to create a top level Session configuration which can then be used throughout an application without the need to repeat the configurational arguments.
 
Base = declarative_base()  # In SQLAlchemy, the declarative_base class is a base class that combines a mapper and a metadata container. The mapper maps a class to a database table and maps instances of the class to records in that table. 

