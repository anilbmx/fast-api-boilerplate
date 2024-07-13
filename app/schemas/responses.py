from pydantic import BaseModel, ConfigDict, EmailStr


class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseResponse):
    user_id: str
    email: EmailStr
