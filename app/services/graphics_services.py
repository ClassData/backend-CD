import os
from io import BytesIO
import matplotlib.pyplot as plt
from .students_service import get_student_by_registration

# Garante que o diretório para salvar os gráficos exista
OUTPUT_DIR = "graficos_gerados"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Gera um gráfico de barras com a média final de cada disciplina para um aluno.
def gerar_grafico_de_linhas(registration: str):
       
    student_data = get_student_by_registration(registration)
    if not student_data:
        return None
    
    disciplinas = [item['disciplina'] for item in student_data]
    medias = [item['media_final'] for item in student_data]

    #criando o grafico 
    plt.figure(figsize=(10, 6))
    plt.bar(disciplinas, medias, color='skyblue')
    plt.ylabel('Média Final')
    plt.title(f'Desempenho por Disciplina - Matrícula: {registration}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # para ser mais eficiente(menos passos), vamos salvar a imagem em um buffer de memoria
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    return img_buffer


    






