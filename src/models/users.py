from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(200))
    password: Mapped[str] = mapped_column(String(200))
