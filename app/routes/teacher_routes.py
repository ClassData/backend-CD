from fastapi import APIRouter, HTTPException, Query
from app.services.teacher_services import *

router = APIRouter(prefix="/teacher",tags=["Students"])

@router.get("")
def get_teacher(
    id: str = Query(None, description="Teacher id")
):
    """
    Retorna as informações do professor
    """
    if id:
        infos = get_teacher_infos(id)
        if not infos:
            raise HTTPException(status_code=404, detail="Teacher not found")
        return infos
    else:
        infos = get_teachers()
        if not infos:
            raise HTTPException(status_code=404, detail="Teachers not found")
        return infos

@router.get("/{registration}/frequency/{subject}")
def get_test(registration: str, subject: str):
    result = get_student_frequency_subject(registration,subject)

    if result is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return result

