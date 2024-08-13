from pydantic import BaseModel, ConfigDict, EmailStr


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class EmployeeResponse(BaseResponse):
    id: int
    name: str
    age: int
    department: str
