from fastapi import FastAPI, Request, HTTPException, Response, Depends
from api.router import router
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from authx import AuthX, AuthXConfig
from pydantic import BaseModel

app = FastAPI(title="Task Manager API for manufactures",
              description="API for Task Manager for manufactures")
app.include_router(router, prefix="/api", tags=["Tasks operations"])
app.mount('/static', StaticFiles(directory='static'), 'static')
templates = Jinja2Templates(directory='templates')

config = AuthXConfig()
config.JWT_SECRET_KEY = 'SECRET_KEY'
config.JWT_ACCESS_COOKIE_NAME = 'my_access_token'
config.JWT_TOKEN_LOCATION = ['cookies']

security = AuthX(config=config)

class UserAddSchema(BaseModel):
    username: str
    password: str
    
class UserSchema(UserAddSchema):
    id: int
    role: str
    
mike = UserSchema(id=1, username="admin", password="123",role='admin')

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(name='index.html', context={'request': request})

@app.post("/login")
def login(creds: UserAddSchema, response: Response):
    if creds.username == "admin" and creds.password == "123":
        token = security.create_access_token(uid=str(mike.id))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail='Incorrect username or password')   
    
@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected(creds: UserSchema, ):
    if creds.role == "admin": 
        return {"data": "TOP SECRET"}
    raise HTTPException(status_code=403)