from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession    
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Date
from datetime import date
from typing import Annotated
from fastapi import Depends

engine = create_async_engine('postgresql+asyncpg://postgres:12042003zZ@localhost:5432/task_manager', echo = True)

new_session = async_sessionmaker(engine, expire_on_commit=False)    

async def get_session():
    async with new_session() as session:
        yield session
        
SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass

class TaskModel(Base):
    __tablename__ = "tasks"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    org_name : Mapped[str] = mapped_column(String)
    task : Mapped[str] = mapped_column(String)
    workshop : Mapped[int] = mapped_column(Integer)
    status : Mapped[int] = mapped_column(Integer)
    begin_date : Mapped[date] = mapped_column(Date)
    dead_line : Mapped[date | None] = mapped_column(Date)

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)  # "user" | "admin"