from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.schemas.user import UserResponse, UserCreate
from app.services.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=['AUTH'])

@router.post('/register',
             response_model=UserResponse,
             status_code=201)
async def register(user_data: UserCreate,
                   session: AsyncSession = Depends(get_async_session)):
    return await AuthService.register(session, user_data)

 