from supabase import create_client, Client
import os
from dotenv import load_dotenv
load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

def get_all_students():
    """
    Retorna todos os alunos cadastrados
    """
    all_students = []
    response = supabase.table("students").select("*").execute()
    for r in response.data:
        # print(f"{r['id']} - {r['registration']} - {r['name']} - {r['age']} - {r['course_id']}")
    
        all_students.append({
            "id": r['id'],
            "matricula": r['registration'],
            "nome": r['name'],
            "idade": r['age'],
            "curso": r['course_id']
        })

    return all_students

 
    
def get_student_by_registration(registration: str):
    """
    Retorna os dados do aluno com a matrícula fornecida, buscando o arquivo Json 
    correspondente na pasta datasets.
    """
    response = supabase.table("students").select("*").eq("registration", registration).execute()

    if response.data:
        r = response.data[0]
        return {
            "id": r['id'],
            "matricula": r['registration'],
            "nome": r['name'],
            "idade": r['age'],
            "curso": r['course_id']
        }
    else:
        print(f"[DEBUG] No student founded for registration: {registration}")
        return None       

def get_student_frequency_subject(registration: str, subject_id: str):
    """
    Calcula a frequência de um aluno em uma disciplina (subject) específica,
    buscando os dados de presença diretamente do banco.
    """
    try:
        response = supabase.table("students") \
            .select("registration, attendance!inner(present, classes!inner(subject_id))") \
            .eq("registration", registration) \
            .eq("attendance.classes.subject_id", subject_id) \
            .execute()

        if not response.data:
            
            student = get_student_by_registration(registration)
            if not student:
                print(f"[DEBUG] Aluno com matrícula {registration} não encontrado.")
                return None 
            
            print(f"[DEBUG] Aluno {registration} não tem registros na disciplina {subject_id}.")
            return {
                "registration": registration,
                "subject_id": subject_id,
                "total_aulas": 0,
                "aulas_presente": 0,
                "frequencia": 0.0
            }
        
        all_records = response.data[0]['attendance']
        total_aulas = len(all_records)

        if total_aulas == 0:
            return {
                "registration": registration,
                "subject_id": subject_id,
                "total_aulas": 0,
                "aulas_presente": 0,
                "frequencia": 0.0
            }

        aulas_presente = len([record for record in all_records if record['present'] == True])
        frequencia = round((aulas_presente / total_aulas) * 100, 2)

        return {
            "registration": registration,
            "subject_id": subject_id,
            "total_aulas": total_aulas,
            "aulas_presente": aulas_presente,
            "frequencia": frequencia
        }
    
    except Exception as e:
        print(f"Erro ao buscar frequência (pode ser UUID inválido): {e}")
        return None 

