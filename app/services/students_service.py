import json
import os

DATA_PATH = "datasets/"  

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

    # Listar os arquivos no diretorio.
    for filename in os.listdir(DATA_PATH):
      
    # Verifica se o nome do arquivo termina com a matrícula
      if filename.endswith(registration_number):
        file_path = os.path.join(DATA_PATH, filename)

        #Abre e le o arquivo Json encontrado
        with open(file_path, "r", encoding="utf-8") as f: 
            student_data = json.load(f)
            return student_data

    print(f'Nenhum arquivo encontrado para a matrícula: {registration}')

    return None


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