import json
import os

DATA_PATH = "datasets"

def get_all_classes():
    """
    Retorna as turmas
    """
    if not os.path.exists(DATA_PATH):
        return None

    file_path = os.path.join(DATA_PATH, "turmas.json")

    if not os.path.exists(file_path):
        return None

    classes_list = []
    with open(file_path, "r", encoding="utf-8") as t:
        classes = json.load(t)

        for c in classes:
            classes_list.append({
                "id": c.get("id"),
                "nome": c.get("disciplina"),
                "turma":c.get("turma"),
                "professor(es)": c.get("professor(es)", []),
                "alunos": c.get("alunos", [])
            })

    return classes_list


def get_class_infos(id: str):
    """
    Retorna a turma pelo id
    """
    if not os.path.exists(DATA_PATH):
        return None

    file_path = os.path.join(DATA_PATH, "turmas.json")

    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as t:
        classes = json.load(t)

        for c in classes:
            if str(c.get("id")) == str(id):
                return {
                    "id": c.get("id"),
                    "nome": c.get("disciplina"),
                    "turma":c.get("turma"),
                    "professor(es)": c.get("professor(es)", []),
                    "alunos": c.get("alunos", [])
                }
                
    print(f"[DEBUG] No classes founded for ID {id}")
    return None