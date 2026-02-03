# Конфигурация авторизации
from authx import AuthX, AuthXConfig

config = AuthXConfig()
config.JWT_SECRET_KEY = 'SECRET_KEY'
config.JWT_ACCESS_COOKIE_NAME = 'my_access_token'
config.JWT_TOKEN_LOCATION = ['cookies']

security = AuthX(config=config)


# Проверка роли
from sqlalchemy import select
from bd.bd_models import UserModel
from bd.bd_core import SessionDep

async def my_autorization(user_id : str, required_role : str, session: SessionDep):
    quarry = select(UserModel.role).where(UserModel.id == int(user_id))
    result = await session.execute(quarry)
    user_role = result.scalar_one_or_none()
    await session.commit()
    if user_role:
        if user_role == required_role:
            return True
        return False
    return None
