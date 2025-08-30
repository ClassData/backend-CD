import json
import os

DATA_PATH = "datasets/Students Performance Dataset.json"  

def get_student_by_registration(registration: str):
    """
    Retorna os dados do aluno com a matrícula fornecida.
    """
    if not os.path.exists(DATA_PATH):
        return None

    with open(DATA_PATH, "r", encoding="utf-8") as f:
         for line in f:
            line = line.strip()
            if not line:
                continue
            student = json.loads(line)
            if student.get("Student_ID") == registration:
                return student
    print("Testando matrícula:", registration, "Arquivo encontrado?", os.path.exists(DATA_PATH))

    return None
