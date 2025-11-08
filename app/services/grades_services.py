from supabase import create_client, Client
import os
from dotenv import load_dotenv
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def get_all_grades(registration: str):
    """
    Retorna TODAS as notas de um aluno, agrupadas por turma e disciplina.
    Esta função foi CORRIGIDA.
    """
    try:
        response = supabase.table("students") \
            .select("registration, name, grades!inner(evaluation_number, value, classes!inner(name, subjects!inner(name)))") \
            .eq("registration", registration) \
            .execute()

        if not response.data:
            print(f"[DEBUG] Aluno {registration} não encontrado ou sem notas.")
            return None
        
        return response.data[0]
    
    except Exception as e:
        print(f"Erro ao buscar todas as notas: {e}")
        return None

def get_student_grades_in_class(registration: str, class_id: str):
    """
    Retorna as 4 notas de um aluno em uma turma (class_id) específica.
    """
    try:
        response = supabase.table("students") \
            .select("registration, grades!inner(evaluation_number, value)") \
            .eq("registration", registration) \
            .eq("grades.class_id", class_id) \
            .order("evaluation_number", referenced_table="grades") \
            .execute()

        if not response.data or not response.data[0].get('grades'):
            print(f"[DEBUG] Nenhuma nota encontrada para matrícula {registration} na turma {class_id}")
            return None 

        return response.data[0]['grades']
    
    except Exception as e:
        print(f"Erro ao buscar notas (pode ser UUID inválido): {e}")
        return None