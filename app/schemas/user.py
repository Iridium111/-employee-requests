from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    login: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    employee_id: int

class UserResponse(BaseModel):
    id: UUID
    employee_id: int

    model_config = ConfigDict(from_attributes=True)

class LoginRequest(BaseModel):
    login: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str