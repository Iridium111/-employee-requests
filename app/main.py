from fastapi import FastAPI

from app.api.router import api_v1_router

app = FastAPI(title="Employee Request Management")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(api_v1_router, prefix="/api/v1")