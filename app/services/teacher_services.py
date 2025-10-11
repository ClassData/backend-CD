import json
import os

DATA_PATH = "datasets"

def get_teachers():
    """
    Retorna todos os professores cadastrados
    """
    if not os.path.exists(DATA_PATH):
        return None

    file_path = os.path.join(DATA_PATH, "professores.json")

    if not os.path.exists(file_path):
        return None

    teachers_list = []
    with open(file_path, "r", encoding="utf-8") as t:
        teachers = json.load(t)

        for teacher in teachers:
            teachers_list.append({
                "id": teacher.get("id"),
                "nome": teacher.get("nome"),
                "disciplinas": teacher.get("disciplinas", [])
            })

    return teachers_list

def get_teacher_infos(id: str):
    """
    Retorna todos os alunos cadastrados
    """
    if not os.path.exists(DATA_PATH):
        return None

    file_path = os.path.join(DATA_PATH, "professores.json")

    if not os.path.exists(file_path):
        print("[DEBUG] Arquivo professores.json não encontrado")
        return None

    with open(file_path, "r", encoding="utf-8") as t:
        teachers = json.load(t)

        for teacher in teachers:
            if str(teacher.get("id")) == str(id):
                return {
                    "id": teacher.get("id"),
                    "nome": teacher.get("nome"),
                    "disciplinas": teacher.get("disciplinas", [])
                }

    print(f"[DEBUG] No teacher founded for ID {id}")
    return None