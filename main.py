from fastapi import FastAPI, Request
from .routers import todos, admin, auth, users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()


templates = Jinja2Templates(directory='TodoApp/templates')


app.mount('/static',StaticFiles(directory='TodoApp/static'), name='static')

@app.get('/')
def test(request:Request):
    return templates.TemplateResponse('home.html',{'request': request}) 

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)


