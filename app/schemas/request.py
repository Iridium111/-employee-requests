from datetime import datetime

from pydantic import BaseModel, ConfigDict
from app.schemas.employee import EmployeeResponse


class RequestCreate(BaseModel):
    description: str
    deadline: datetime
    author_id: int
    executor_id: int


class RequestResponse(BaseModel):
    number: str
    description: str
    deadline: datetime
    status: str
    author: EmployeeResponse
    executor: EmployeeResponse

    model_config = ConfigDict(from_attributes=True)


class RequestUpdate(BaseModel):
    description: str | None = None
    deadline: datetime | None = None
    executor_id: int | None = None


class RequestChangeStatus(BaseModel):
    status: str

