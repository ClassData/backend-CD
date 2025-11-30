from supabase import create_client, Client
import os
from dotenv import load_dotenv
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def get_all_classes():
    """
    Retorna as turmas
    """
    classes_list = []
    classes = supabase.table("classes").select("*").execute()
    print(classes)
    for c in classes.data:
        print(f"{c['id']} - {c['name']} - {c['subject_id']}")

        classes_list.append({
                "id": c['id'],
                "nome": c['name'],
                "turma":c['subject_id'],
            })

    return classes_list


def get_class_infos(id: str):
    """
    Retorna a turma pelo id
    """

    classes = supabase.table("classes").select("*").eq("id", id).execute()

    if classes.data:
        c = classes.data[0]
        return {
            "id": c['id'],
            "nome": c['name'],
            "disciplina": c['subject_id'],
        }
    else:
        print(f"[DEBUG] Nenhuma turma encontrada com ID {id}")
        return None