from pydantic import BaseModel, EmailStr


class BaseRequest(BaseModel):
    # may define additional fields or config shared across requests
    pass


class PetCreateRequest(BaseRequest):
    name: str
    place: str
    type: str
