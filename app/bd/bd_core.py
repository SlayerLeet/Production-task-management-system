from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession    
from typing import Annotated
from fastapi import Depends


engine = create_async_engine('postgresql+asyncpg://postgres:12042003zZ@localhost:5432/task_manager', echo = True)

new_session = async_sessionmaker(engine, expire_on_commit=False)    

async def get_session():
    async with new_session() as session:
        yield session
        
SessionDep = Annotated[AsyncSession, Depends(get_session)]