import json
import os
import numpy as np

DATA_PATH = "datasets/alunos"

def get_all_students():
    """
    Retorna todos os alunos cadastrados
    """
    if not os.path.exists(DATA_PATH):
        return None
    
    all_students= []
    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".json"):
            # divide o nome em partes do arquivo em partes  (ex: "Nome_Completo_12345.json")
            try:
                parts = filename.replace(".json", "").split("_")
                registration = parts[-1]
                
                # O nome é todo o resto, unido por espaços
                nome_completo = " ".join(parts[:-1])

                student_data = {
                    "matricula": registration,
                    "nomeCompleto": nome_completo,
                    "coeficiente": calculate_student_overall_avarege(registration).get("Média geral do aluno"),
                    "frequenciaMedia": get_student_frequency_average(registration).get("Média de frequências")
                }
                all_students.append(student_data)
            except (IndexError, ValueError) as e:
                print(f"[AVISO] O arquivo '{filename}' não segue o padrão de nome esperado e foi ignorado.")

    return all_students

 
    
def get_student_by_registration(registration: str):
    """
    Retorna os dados do aluno com a matrícula fornecida, buscando o arquivo Json 
    correspondente na pasta datasets.
    """
   
    if not os.path.isdir(DATA_PATH):
         print(f"Erro: O diretório '{DATA_PATH}' não foi encontrado.")
         return 
    
    expected_filename_suffix = f"_{registration}.json"

    for filename in os.listdir(DATA_PATH):
        if filename.endswith(expected_filename_suffix):
            file_path = os.path.join(DATA_PATH, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    disciplinas_data = json.load(f)
                
                # Extrai o nome completo do aluno a partir do nome do arquivo
                nome_completo = filename.replace(expected_filename_suffix, "").replace("_", " ")

                return {
                    "matricula": registration,
                    "nomeCompleto": nome_completo,
                    "disciplinas": disciplinas_data
                }
            except (IOError, json.JSONDecodeError) as e:
                print(f"Erro ao ler ou decodificar o arquivo {filename}: {e}")
                return None
    return None         

def get_student_frequency_subject(registration: str,subject: str):
  student_data = get_student_by_registration(registration)
  if not student_data:
      return None

  final_frequencies = []
  for disciplina in student_data["disciplinas"]:
      freq = disciplina.get("frequencia_total")
      if freq:
          try:
              freq_value = float(freq.replace("%", ""))
              final_frequencies.append(freq_value)
          except ValueError:
              pass  

  if not final_frequencies:
      return {"Matricula": registration, "Média de frequências": 0}

  overall_average = sum(final_frequencies) / len(final_frequencies)

  return {"Matricula": registration, "Média de frequências": round(overall_average, 2)}


def get_student_frequency_average(registration: str):
  """
  Retorna a media de frequencia do aluno com a matrícula fornecida
  """
  student_data = get_student_by_registration(registration)
  if not student_data:
      return None

  final_frequencies = []
  for disciplina in student_data["disciplinas"]:
      freq = disciplina.get("frequencia_total")
      if freq:
          try:
              freq_value = float(freq.replace("%", ""))
              final_frequencies.append(freq_value)
          except ValueError:
              pass  

  if not final_frequencies:
      return {"Matricula": registration, "Média de frequências": 0}

  overall_average = sum(final_frequencies) / len(final_frequencies)

  return {"Matricula": registration, "Média de frequências": round(overall_average, 2)}

def get_student_frequency_subject(registration: str,subject: str):
  student_data = get_student_by_registration(registration)
  if not student_data:
      return None

  final_frequencies = []
  for disciplina in student_data:
      freq = disciplina.get("frequencia_total")
      if freq:
          try:
              freq_value = float(freq.replace("%", ""))
              final_frequencies.append(freq_value)
          except ValueError:
              pass  

  if not final_frequencies:
      return {"Matricula": registration, "Média de frequências": 0}

  overall_average = sum(final_frequencies) / len(final_frequencies)

  return {"Matricula": registration, "Média de frequências": round(overall_average, 2)}
  return None

def get_student_frequency_average(registration: str):
  """
  Retorna a media de frequencia do aluno com a matrícula fornecida
  """
  student_data = get_student_by_registration(registration)
  if not student_data:
      return None

  final_frequencies = []
  for disciplina in student_data:
      freq = disciplina.get("frequencia_total")
      if freq:
          try:
              freq_value = float(freq.replace("%", ""))
              final_frequencies.append(freq_value)
          except ValueError:
              pass  

  if not final_frequencies:
      return {"Matricula": registration, "Média de frequências": 0}

  overall_average = sum(final_frequencies) / len(final_frequencies)

  return {"Matricula": registration, "Média de frequências": round(overall_average, 2)}

def calculate_student_overall_avarege(registration: str):
    """
    Calcula a média de um aluno a partir dos dados de notas.
    """

    student_data = get_student_by_registration(registration)
    if not student_data:
        return None
    
    # vamos pegar a media final de todas as disciplinas dos alunos 
    final_grades = []
    for disciplinas in student_data["disciplinas"]:
       if "media_final" in disciplinas:
          final_grades.append(disciplinas['media_final'])

    # se não tiver notas, não calcula      
    if not final_grades:
      return {"Matricula": registration, "média geral do aluno": 0}   

    # media geral de todas as disciplinas
    overall_average = sum(final_grades) / len(final_grades)

    # retorna o resultado 
    return {"Matricula": registration, "Média geral do aluno": round(overall_average, 2)}