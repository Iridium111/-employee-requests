from fastapi import FastAPI

app = FastAPI(title="Employee Request Management")

@app.get("/health")
async def health_check():
    return {"status": "ok"}