from fastapi import FastAPI
from app.routes import api_router
from app.routes import graphics_routes

app = FastAPI(title="Class Data API", version="1.0.0")

app.include_router(graphics_routes.router)

# Register all routes
app.include_router(api_router)