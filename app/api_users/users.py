from fastapi import Response, APIRouter, Cookie, Depends, HTTPException, Request
from api_users.auth import security, config, my_autorization
from authx import TokenPayload
from authx.token import decode_token
from api_users.schemas import UserAddSchema, UserSchema
from bd.bd_core import SessionDep
from bd.bd_models import UserModel, UserRoles
from sqlalchemy import select, and_
from typing import Optional


users = APIRouter()



@users.post("/registration")
async def registration(data: UserAddSchema, response: Response, session: SessionDep):
    # DB moment
    new_user = UserModel(username = data.username,
                         password = data.password)
    session.add(new_user)
    quarry = select(UserModel.role).where(UserModel.username == data.username and UserModel.password == data.password)
    await session.execute(quarry)
    await session.commit()
    
    role_of_user = 'USER'
    
    # return token with id
    token = security.create_access_token(uid=role_of_user)
    response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
    return {"access_token": token}
     

@users.post("/login")
async def login(creds: UserAddSchema, response: Response, session: SessionDep):
    quarry = select(UserModel).where(
        and_(UserModel.username == creds.username,
             UserModel.password == creds.password))
    result = await session.execute(quarry)
    user = result.scalar_one_or_none()
    
    if user:
        token = security.create_access_token(uid=str(user.id))
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail='Incorrect username or password')   
    
@users.get("/protected", dependencies=[Depends(security.access_token_required)])
async def protected(request: Request, _=Depends(security.access_token_required)):
    payload = request.state.user  # TokenPayload
    uid = payload.sub             # или payload["uid"]
    return {"data": uid}

@users.get("/debug")
async def debug(session: SessionDep, request: Request, _=Depends(security.access_token_required)):
    token = request.cookies.get("my_access_token")  # или из header
    
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")
    
    payload = decode_token(
    token=token,
    key=config.JWT_SECRET_KEY or 'SECRET_KEY',
    algorithms=[config.JWT_ALGORITHM],
    )
    
    uid = payload.get("sub")
    
    can = await my_autorization(user_id=str(uid), required_role=UserRoles.USER.name, session=session)
    print(can)
    if can:
        if can == True:
            return {"message" : f"проходите, все четко ваша роль - , требуемая роль - {UserRoles.USER.name}"}
        raise HTTPException(status_code=(403), detail="У вас нет прав для доступа к этой команде")
    raise HTTPException(status_code=401, detail='такого пользователя не существует') 

    

