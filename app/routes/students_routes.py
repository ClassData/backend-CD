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

@router.get("/students/registrations")
def get_all_student_registrations():
    """
    Retorna uma lista com TODAS as matrículas cadastradas no banco.
    Útil para verificar quais alunos existem antes de tentar gerar gráficos.
    """
    try:
        # Busca apenas a coluna 'registration' da tabela 'students'
        response = supabase.table("students").select("registration").execute()
        
        if not response.data:
            return {"message": "Nenhum aluno encontrado no banco.", "registrations": []}

        # Transforma de [{'registration': '123'}, {'registration': '456'}]
        # Para uma lista simples: ['123', '456']
        lista_matriculas = [aluno['registration'] for aluno in response.data]
        
        return {
            "total": len(lista_matriculas),
            "registrations": lista_matriculas
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar matrículas: {str(e)}")