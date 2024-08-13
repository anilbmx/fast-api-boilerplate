from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import Session
from app.utils.database_session import get_async_session
from app.models.employee import Employee
from app.schemas.requests import EmployeeCreate
from app.schemas.responses import UserResponse
from app.utils.auth import keycloak_authenticate
from sqlalchemy.exc import IntegrityError
# from app.utils.auth import auth_user

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)


# @router.get("/fetch", dependencies=[Depends(auth_user)], response_model=UserResponse, description="Get all pets")
@router.get("/fetch", response_model=UserResponse, description="Get all pets")
async def get_all_employees(
    skip: int = 0,
    limit: int = 10,
    user: dict[str] = Depends(keycloak_authenticate),
    db: AsyncSession = Depends(get_async_session)
    ):
    """
    To get all employees details list saved
    
    returns
        Employees - list of employees
    """
    stmt = select(Employee).offset(skip).limit(limit)
    result = await db.execute(stmt)
    employees = result.scalars().all()
    return employees

@router.post("/save", response_model=UserResponse, description="Create pets")
async def create_employee(
    employee: EmployeeCreate,
    user: dict[str] = Depends(keycloak_authenticate),
    db: AsyncSession = Depends(get_async_session)):
    # Create an Employee instance
    db_employee = Employee(
        name=employee.name,
        age=employee.age,
        department=employee.department
    )
    
    # Add and commit the new employee to the database
    db.add(db_employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Employee already exists")
    
    return db_employee