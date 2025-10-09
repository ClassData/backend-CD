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


# rota criada para a função de média geral do aluno (em todas as disciplinas)
# ex: http://127.0.0.1:8000/students/44335/media-geral
@router.get("/{registration}/media-geral")
def get_overall_average_route(registration: str):
    """
    Retorna a média geral de um aluno em todas as disciplinas.
    """
    result = calculate_student_overall_avarege(registration)

    if result is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return result
