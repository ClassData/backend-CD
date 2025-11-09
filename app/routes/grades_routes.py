from fastapi import APIRouter, HTTPException, Query
from app.services.grades_services import get_all_grades, get_student_grades_in_class

router = APIRouter(prefix="/grades",tags=["Grades"])

@router.get("/")
def get_student_all_grades_route(
    registration: str = Query(..., description="Student registration number")
):
    """
    Retorna TODAS as notas de um aluno em todas as turmas,
    dado o 'registration' (matrícula).
    Esta rota foi CORRIGIDA.
    """
    if not registration:
        raise HTTPException(status_code=400, detail="Student registration is required")

    student_grades = get_all_grades(registration)
    if not student_grades:
        raise HTTPException(status_code=404, detail="Student not found or no grades registered")
    
    return student_grades


@router.get("/{registration}/{class_id}")
def get_student_grades_in_class_route(registration: str, class_id: str):
    """
    Retorna as 4 notas de um aluno para uma TURMA (class_id) específica.
    """
    grades = get_student_grades_in_class(registration, class_id)
    
    if grades is None:
        # Isso cobre aluno não encontrado OU aluno não matriculado na turma
        raise HTTPException(status_code=404, detail="Grades not found. Check if registration and class_id are correct.")

    return {
        "registration": registration,
        "class_id": class_id,
        "grades": grades
    }

#    curl -X GET "http://localhost:8000/grades/150001/685f4e66-7a47-4f93-814a-04746f0954a7"