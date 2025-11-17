from supabase import create_client, Client
import os
from dotenv import load_dotenv
from collections import defaultdict

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



def get_teacher_classes_service(teacher_id: str):
    """
    Busca todas as turmas de um professor e os dados das turmas.
    """

    try:
        response_teacher_classes = supabase.table("classes_teachers") \
                                    .select("class_id, created_at, updated_at") \
                                    .eq("teacher_id", teacher_id) \
                                    .execute()
    
        if not response_teacher_classes.data:
            print(f"[DEBUG] Professor {teacher_id} não encontrado ou sem turmas.")
            return None 

        print(f"Resposta da Query 1 (Turmas do Prof): {response_teacher_classes.data}")

        final_class_list = []
        
        for teacher_class_entry in response_teacher_classes.data:
            class_id = teacher_class_entry['class_id']
            
            class_info_resp = supabase.table("classes") \
                                 .select("name") \
                                 .eq("id", class_id) \
                                 .single() \
                                 .execute()
            class_name = class_info_resp.data.get('name') if class_info_resp.data else 'N/A'

            students_resp = supabase.table("classes_students") \
                               .select("students!inner(id, name, registration)") \
                               .eq("class_id", class_id) \
                               .execute()
            
            grades_resp = supabase.table("grades") \
                              .select("student_id, evaluation_number, value") \
                              .eq("class_id", class_id) \
                              .execute()

            attendance_resp = supabase.table("attendance") \
                                .select("student_id, date, present") \
                                .eq("class_id", class_id) \
                                .execute()

            all_grades_list = grades_resp.data if grades_resp.data else []
            all_attendance_list = attendance_resp.data if attendance_resp.data else []
            students_list = students_resp.data if students_resp.data else []

            if not students_list:
                print(f"[DEBUG] Query de 'classes_students' para a turma {class_id} veio vazia.")

            grades_map = defaultdict(list)
            for g in all_grades_list:
                grades_map[g['student_id']].append({
                    "evaluation_number": g['evaluation_number'],
                    "value": g['value']
                })
            
            attendance_map = defaultdict(list)
            for a in all_attendance_list:
                attendance_map[a['student_id']].append({
                    "date": a['date'],
                    "present": a['present']
                })

            final_students = []
            for student_entry in students_list:
                student = student_entry.get('students')
                if not student:
                    continue
                
                student_uuid = student['id']
                final_students.append({
                    "student_registration": student['registration'],
                    "student_name": student['name'],
                    "student_uuid": student_uuid,
                    "attendances": attendance_map.get(student_uuid, []),
                    "grades": grades_map.get(student_uuid, [])
                })

            final_class_list.append({
                "class_id": class_id,
                "class_name": class_name,
                "teacher_id": teacher_id,
                "students": final_students,
                "created_at": teacher_class_entry['created_at'],
                "updated_at": teacher_class_entry['updated_at']
            })

        if not final_class_list:
            print("[DEBUG] Nenhuma turma com dados válidos foi processada.")
            return None

        return final_class_list

    except Exception as e:
        print(f"Erro ao buscar dados complexos do professor: {e}")
        return None