from supabase import create_client, Client
import os
from dotenv import load_dotenv
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def get_teachers():
    """
        Retorna todos os professores cadastrados
    """

    teachers_list = []
    teachers = supabase.table("teachers").select("*").execute()
    print("\n=== Professores ===")
    for t in teachers.data:
        print(f"{t['id']} - {t['name']} - {t['age']} - {t['department_id']}")

        teachers_list.append({
            "id": t['id'],
            "nome": t['name'],
            "disciplinas": t['age'],
            "departamento": t['department_id']
        })

    return teachers_list

def get_teacher_infos(id: str):
    """
    Retorna todos os alunos cadastrados
    """
    response = supabase.table("teachers").select("*").eq("id", id).execute()

    if response.data:
        t = response.data[0]
        return {
            "id": t['id'],
            "nome": t['name'],
            "disciplinas": t['age'],
            "departamento": t['department_id']
        }
    else:
        print(f"[DEBUG] No teacher founded for ID {id}")
        return None