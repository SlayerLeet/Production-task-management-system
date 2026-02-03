from fastapi import FastAPI, Request, HTTPException, Response, Depends
from api_tasks.tasks import tasks
from api_users.users import users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Task Manager API for manufactures",
              description="API for Task Manager for manufactures")
app.include_router(tasks, prefix="/tasks", tags=["Tasks operations"])
app.include_router(users, prefix="/users", tags=["Users operations"])
app.mount('/static', StaticFiles(directory='static'), 'static')
templates = Jinja2Templates(directory='templates')


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(name='index.html', context={'request': request})

