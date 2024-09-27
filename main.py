from fastapi import FastAPI, Request, status
from routers import todos, admin, auth, users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from database import Base, engine

# to Create database 
Base.metadata.create_all(bind=engine)

app = FastAPI()


app.mount('/static',StaticFiles(directory='static'), name='static')

@app.get('/')
def test(request:Request):
    return RedirectResponse(url='/todos/todo-page', status_code=status.HTTP_302_FOUND)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)


