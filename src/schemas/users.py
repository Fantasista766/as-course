from pydantic import BaseModel, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(UserLogin):
    first_name: str
    last_name: str


class UserAdd(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserWithHashedPassword(User):
    hashed_password: str
