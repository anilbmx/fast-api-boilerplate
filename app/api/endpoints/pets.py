from fastapi import APIRouter, Depends, status
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Pets
from app.schemas.requests import PetCreateRequest
from app.schemas.responses import UserResponse
from app.utils.auth import auth_user

router = APIRouter(
    prefix="/v1/pets",
    tags=["Pets"]
)


@router.get("/pets", dependencies=[Depends(auth_user)], response_model=UserResponse, description="Get all pets")
async def get_all_pets() -> Pets:
    pets = select(Pets)
    return pets

@router.post("/pets", response_model=UserResponse, description="Create pets")
async def create_pets(pets: PetCreateRequest, session: AsyncSession):
    stmt = insert(Pets).values(name=pets.name, type=pets.type, place=pets.place)
    return stmt


