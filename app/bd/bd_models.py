from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Date
from datetime import date
from api_users.schemas import UserRoles

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
    password: Mapped[str] = mapped_column(String)
    role: Mapped[UserRoles] = mapped_column(String, default=UserRoles.USER.name)