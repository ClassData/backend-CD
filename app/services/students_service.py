import json
import os

DATA_PATH = "datasets/alunos"

def get_all_students():
    """
    Retorna todos os alunos cadastrados
    """
    if not os.path.exists(DATA_PATH):
        return None

    return None
    
# rota criada
# ex: http://127.0.0.1:8000/students/?registration=44335
def get_student_by_registration(registration: str):
    """
    Retorna os dados do aluno com a matrícula fornecida, buscando o arquivo Json 
    correspondente na pasta datasets.
    """
    if not os.path.exists(DATA_PATH):
        return None

    #pega o final do nome do arquivo Json
    registration_number = f"_{registration}.json"
    print(f"[DEBUG] Procurando matrícula {registration} -> {registration_number}")

    # Listar os arquivos no diretorio.
    for filename in os.listdir(DATA_PATH):
      
    # Verifica se o nome do arquivo termina com a matrícula
      if filename.endswith(registration_number):
        file_path = os.path.join(DATA_PATH, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            disciplinas = json.load(f)
            print(f"[DEBUG] Encontrado arquivo para matrícula {registration}: {filename}")
            
            # Calcula coeficiente e presença média
            total_notas = 0
            total_presenca = 0
            count_notas = 0
            count_presenca = 0

            for d in disciplinas:
                total_notas += sum(d["notas_bimestre"])
                count_notas += len(d["notas_bimestre"])

                total_presenca += sum(d["frequencia_bimestre"])
                count_presenca += len(d["frequencia_bimestre"])

            coeficiente = round(total_notas / count_notas, 2) if count_notas else 0
            presenca_media = round(total_presenca / count_presenca, 2) if count_presenca else 0

            # Extrai nome do aluno do arquivo (supondo que esteja no nome do arquivo)
            # Ex: "FulanoCiclanodense_839274.json" -> nome completo = "Fulano Ciclanodense"
            nome_completo = filename.replace(f"_{registration}.json", "").replace("_", " ")

            return {
                "matricula": registration,
                "nomeCompleto": nome_completo,
                "coeficiente": coeficiente,
                "presencaMedia": presenca_media,
                "disciplinas": disciplinas
            }

    return None

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

# rota criada 
# ex: http://127.0.0.1:8000/students/44335/media-geral
def calculate_student_overall_avarege(registration: str):
    """
    Calcula a média de um aluno a partir dos dados de notas.
    """

    student_data = get_student_by_registration(registration)
    if not student_data:
        return None
    
    # vamos pegar a media final de todas as disciplinas dos alunos 
    final_grades = []
    for disciplinas in student_data:
       if "media_final" in disciplinas:
          final_grades.append(disciplinas['media_final'])

    # se não tiver notas, não calcula      
    if not final_grades:
      return {"Matricula": registration, "média geral do aluno": 0}   

    # media geral de todas as disciplinas
    overall_average = sum(final_grades) / len(final_grades)

    # retorna o resultado 
    return {"Matricula": registration, "Média geral do aluno": round(overall_average, 2)}