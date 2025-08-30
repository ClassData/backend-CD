from fastapi import FastAPI
from app.routes import api_router
from app import config
import os
import sys

app = FastAPI(
    title="Class Data API",
    version="1.0.0",
    description="Backend API for monitoring students, classes, subjects, grades and statistics"
)

# Register all routes
app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Welcome to Class Data API"}



if __name__ == "__main__":
    if config.DEBUG:
        os.execv(sys.executable, [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--reload",
            "--host", config.HOST,
            "--port", str(config.PORT)
        ])
    else:
        import uvicorn
        uvicorn.run(app, host=config.HOST, port=config.PORT)