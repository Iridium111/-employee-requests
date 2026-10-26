from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_async_session
from app.core.security import create_access_token, create_refresh_token
from app.repositories.user import UserRepository
from app.schemas.user import UserResponse, UserCreate, LoginRequest, TokenResponse, RefreshTokenRequest
from app.services.auth_service import AuthService

router = APIRouter(prefix='/auth', tags=['AUTH'])

@router.post('/register',
             response_model=UserResponse,
             status_code=201)
async def register(user_data: UserCreate,
                   session: AsyncSession = Depends(get_async_session)):
    return await AuthService.register(session, user_data)

@router.post('/login',
             response_model=TokenResponse)
async def login(credentials: LoginRequest,
                session: AsyncSession = Depends(get_async_session)):
    user = await AuthService.login(session, credentials)

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    await UserRepository.update_refresh_token(session, user.id, refresh_token)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token)

@router.post('/logout',
             status_code=204)
async def logout(request: RefreshTokenRequest,
                 session: AsyncSession = Depends(get_async_session)) -> None:
    await AuthService.logout(session,
                             request.refresh_token)

@router.post('/refresh',
             response_model=TokenResponse)
async def refresh(request: RefreshTokenRequest,
                  session: AsyncSession = Depends(get_async_session)):
    return await AuthService.refresh(session,
                               request.refresh_token)