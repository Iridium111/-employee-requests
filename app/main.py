from fastapi import FastAPI

from app.api.router import api_v1_router
from app.core.exception_handlers import (login_exists_handler,
                                         email_exists_handler,
                                         employee_registered_handler,
                                         employee_not_found_handler)
from app.core.exceptions import (LoginAlreadyExistsError,
                                 EmailAlreadyExistsError,
                                 EmployeeAlreadyRegisteredError,
                                 EmployeeNotFoundError)

app = FastAPI(title="Employee Request Management")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(api_v1_router, prefix="/api/v1")

app.add_exception_handler(LoginAlreadyExistsError,
                          login_exists_handler)
app.add_exception_handler(EmailAlreadyExistsError,
                          email_exists_handler)
app.add_exception_handler(EmployeeAlreadyRegisteredError,
                          employee_registered_handler)
app.add_exception_handler(EmployeeNotFoundError,
                          employee_not_found_handler)