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