from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (LoginAlreadyExistsError,
                                 EmailAlreadyExistsError,
                                 EmployeeAlreadyRegisteredError,
                                 EmployeeNotFoundError)

async def login_exists_handler(request: Request,
                               exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content={'detail': 'Login already exists.'})

async def email_exists_handler(request: Request,
                               exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content={'detail': 'Email already exists.'})

async def employee_registered_handler(request: Request,
                                      exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content={'detail': 'Employee already registered.'})

async def employee_not_found_handler(request: Request,
                                     exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                        content={'detail': 'Employee not found.'})

async def wrong_login_or_password_handler(request: Request,
                                          exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                        content={'detail': 'Wrong login or password.'},
                        headers={"WWW-Authenticate": "Bearer"})

async def wrong_refresh_token_handler(request: Request,
                                      exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                        content={'detail': 'Wrong refresh token.'},
                        headers={"WWW-Authenticate": "Bearer"})