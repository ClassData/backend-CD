'''
    Codigo de requisicoes do banco de dados que esta hospedado no Supabase
'''

from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

# Get Departamentos
departments = supabase.table("department").select("*").execute()
print("\n=== DEPARTAMENTOS ===")
for d in departments.data:
    print(f"{d['id']} - {d['name']}")

# Get Cursos
courses = supabase.table("courses").select("*").execute()
print("\n=== CURSOS ===")
for c in courses.data:
    print(f"{c['id']} - {c['name']} (Departamento: {c['department_id']})")

print("\n=== CURSOS + DEPARTAMENTO ===")
for c in courses.data:
    dept_name = next(
        (d["name"] for d in departments.data if d["id"] == c["department_id"]),
        "Desconhecido"
    )
    print(f"{c['name']} -> Departamento: {dept_name}")


# Get Professores
teachers = supabase.table("teachers").select("*").execute()
print("\n=== Professores ===")
for t in teachers.data:
    print(f"{t['id']} - {t['name']} - {t['age']} - {t['department_id']}")

# Get Estudantes
students = supabase.table("students").select("*").execute()
print("\n=== Estudantes ===")
for s in students.data:
    print(f"{c['id']} - {c['registration']} - {c['name']} - {c['age']} - {c['couse_id']}")
    
# Get Notas
grades = supabase.table("grades").select("*").execute()
print("\n=== Notas ===")
for g in grades.data:
    print(f"{g['id']} - {g['student_id']} - {g['class_id']} - {g['evaluation_number']} - {g['value']}")\

# Get Turmas
classes = supabase.table("classes").select("*").execute()
print("\n=== Turmas ===")
for c in classes.data:
    print(f"{c['id']} - {c['name']} - {c['subject_id']}")

# Get Professores e suas turmas
classes_teachers = supabase.table("classes_teachers").select("*").execute()
print("\n=== Professores e suas Turmas ===")
for t in classes_teachers.data:
    print(f"{t['class_id']} - {t['teacher_id']}")

# Get Estudantes e suas turmas
classes_students = supabase.table("classes_students").select("*").execute()
print("\n=== Estudante e suas Turmas ===")
for t in classes_students.data:
    print(f"{t['class_id']} - {t['student_registration']}")

# Get Presencas
attendance = supabase.table("attendance").select("*").execute()
print("\n=== Presencas ===")
for a in attendance.data:
    print(f"{a['id']} - {a['student_id']} - {a['class_id']} - {a['date']} - {a['present']}")