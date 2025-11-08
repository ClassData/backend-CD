from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api_router, students_routes, teacher_routes, graphics_routes, classes_routes, grades_routes

app = FastAPI(title="Class Data API", version="1.0.0")

# CORS
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ou ["*"] para liberar todos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra rotas
app.include_router(api_router)
app.include_router(students_routes.router)
app.include_router(graphics_routes.router)
app.include_router(teacher_routes.router)
app.include_router(classes_routes.router)
app.include_router(grades_routes.router)

