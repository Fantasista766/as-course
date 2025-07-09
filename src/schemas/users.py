from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserLoginDTO(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserRegisterDTO(UserLoginDTO):
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)


class UserAddDTO(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str


class UserDTO(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPasswordDTO(UserDTO):
    hashed_password: str
