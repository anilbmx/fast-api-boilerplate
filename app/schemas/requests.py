from pydantic import BaseModel, EmailStr


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass

class EmployeeCreate(BaseRequest):
    name: str
    age: int
    department: str
