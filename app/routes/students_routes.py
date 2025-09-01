from fastapi import APIRouter, HTTPException, Query
from app.services.students_service import get_student_by_registration, calculate_student_overall_avarege

router = APIRouter(prefix="/students",tags=["Students"])

@router.get("/")
def get_student(registration: str = Query(..., description="Student registration number")):
    """
    Retorna os dados de cadastro de um aluno pela matrícula
    """
    student = get_student_by_registration(registration)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student