from pydantic import BaseModel


class UserRequestAdd(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserAdd(BaseModel):
    first_name: str
    last_name: str
    email: str
    hashed_password: str


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True
