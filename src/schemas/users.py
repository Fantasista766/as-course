from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserRegister(UserLogin):
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)


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

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str
