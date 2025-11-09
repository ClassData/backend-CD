from fastapi import APIRouter, HTTPException, Query
from app.services.students_service import *

router = APIRouter(prefix="/students",tags=["Students"])

@router.get("/")
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