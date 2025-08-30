from fastapi import FastAPI
from app.routes import api_router

app = FastAPI(title="Class Data API", version="1.0.0")

# Register all routes
app.include_router(api_router)