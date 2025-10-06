from fastapi import APIRouter, HTTPException, Query
from app.services.students_service import *

router = APIRouter(prefix="/students",tags=["Students"])

@router.get("")
def get_student(
    registration: str = Query(None, description="Student registration number")
):
    """
    Retorna todos os estudantes ou apenas um se 'registration' for informado
    """
    if registration:
        student = get_student_by_registration(registration)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
    else:
        students = get_all_students()
        if not students:
            raise HTTPException(status_code=404, detail="No students found")
        return students

@router.get("/{registration}/frequency/{subject}")
def get_frequency_subject_route(registration: str, subject: str):
    result = get_student_frequency_subject(registration,subject)

    if result is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return result

@router.get("/{registration}/frequency")
def get_frequencys_route(registration: str):
    result = get_student_frequency_average(registration)

    if result is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return result

# rota criada para a função de média geral do aluno (em todas as disciplinas)
@router.get("/{registration}/media-geral")
def get_overall_average_route(registration: str):
    """
    Retorna a média geral de um aluno em todas as disciplinas.
    """
    result = calculate_student_overall_avarege(registration)

    if result is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return result
