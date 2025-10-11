import os
from io import BytesIO
import matplotlib
matplotlib.use('Agg') # usa um renderizador de alta qualidade sem precisar de uma janela de exibição
import matplotlib.pyplot as plt
import numpy as np
import json

from .students_service import get_student_by_registration

# Garante que o diretório para salvar os gráficos exista
OUTPUT_DIR = "graficos_gerados"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Gera um gráfico de barras com a média final de cada disciplina para um aluno.
def gerar_grafico_de_linhas(registration: str):
       
    student_data = get_student_by_registration(registration)

    if not student_data or 'disciplinas' not in student_data:
        return None

    #criando o grafico 
    plt.figure(figsize=(12, 7))

    for disciplina_info in student_data['disciplinas']:
        nome_disciplina = disciplina_info.get('disciplina')
        notas_bimestre = disciplina_info.get('notas_bimestre')

     # Garante que a disciplina tem um nome e uma lista de notas para plotar
        if nome_disciplina and notas_bimestre:
            # Cria o eixo X (os bimestres) dinamicamente
            bimestres = [f'{i+1}º Bimestre' for i in range(len(notas_bimestre))]
            # Plota a linha para a disciplina atual
            plt.plot(bimestres, notas_bimestre, marker='o', linestyle='-', label=nome_disciplina)   

    plt.title(f"'Evolução de Notas por Bimestre - Matrícula: {registration}")  
    plt.ylabel('Nota')
    plt.xlabel('Período')
    plt.ylim(0, 10.5)  # Define o limite do eixo Y de 0 a 10.5
    plt.grid(True, linestyle='--', alpha=0.7) # Adiciona uma grade para facilitar a leitura

     # Adiciona a legenda do lado de fora do gráfico para não atrapalhar a visualização
    plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
    
    # Ajusta o layout para garantir que a legenda não seja cortada
    plt.tight_layout(rect=[0, 0, 0.85, 1])

    # para ser mais eficiente(menos passos), vamos salvar a imagem em um buffer de memoria
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    return img_buffer


# visualizar a correlação entre a frequencia total e a media final de cada disciplina
def gerar_grafico_frequencia_x_notas(registration: str):

     # logica de pegar os dados e analisar eles 
    student_data = get_student_by_registration(registration)
    if not student_data or 'disciplinas' not in student_data:
        return None
    
    frequencias = []
    media_finais = []
    nomes_das_disciplinas = []

    for disciplina in student_data[ 'disciplinas']:
        freq = disciplina.get("frequencia_total")
        media = disciplina.get("media_final")
        nome = disciplina.get("disciplina")
        
        if freq and media is not None:
            try: 
                frequencia_float = float(freq.replace('%', ''))
                frequencias.append(frequencia_float)
                media_finais.append(media)
                nomes_das_disciplinas.append(nome)
            except(ValueError, TypeError):
                continue

    #criando o grafico 
    plt.figure(figsize=(10, 6))
    plt.scatter(frequencias, media_finais, color='dodgerblue', alpha=0.7)

    # Adiciona o nome da disciplina perto de cada ponto para identificação
    for i, txt in enumerate(nomes_das_disciplinas):
        plt.annotate(txt, (frequencias[i], media_finais[i]), textcoords="offset points", xytext=(0,5), ha='center', fontsize=8)

    # Melhorando a aparencia
    plt.title(f'Relação Frequência vs. Nota Final - Matrícula {registration}')
    plt.xlabel('Frequência Total (%)')
    plt.ylabel('Média Final')
    plt.xlim(min(frequencias) - 2, 100) # Limites do eixo X
    plt.ylim(0, 10.5) # Limites do eixo Y
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Salva no buffer de memória
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    return img_buffer

# grafico de pizza 
def status_de_aprovação_pizza(registration: str):
  
    student_data = get_student_by_registration(registration)
    if not student_data or 'disciplinas' not in student_data:
        return None

    
    # Dicionário para contar status (para o gráfico de pizza)
    contadores_de_condicao = {'Aprovado': 0, 'Reprovado': 0}
    for c in student_data['disciplinas']:
        condicao = c.get('status_aprovacao')
        if condicao in contadores_de_condicao:
            contadores_de_condicao[condicao] += 1
    
    # Listas com os nomes das disciplinas (para o texto)
    aprovadas = [d['disciplina'] for d in student_data['disciplinas'] if d.get('status_aprovacao') == 'Aprovado']
    reprovadas = [d['disciplina'] for d in student_data['disciplinas'] if d.get('status_aprovacao') == 'Reprovado']

    # cria e controla a largura das duas seções do grafico
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), gridspec_kw={'width_ratios': [1.2, 1]})

    # fazendo o grafico de pizza
    labels = contadores_de_condicao.keys()
    sizes = contadores_de_condicao.values()
    colors = ['green', 'red']
    
    # Logica para não plotar fatias com valor zero
    if 0 in sizes:
        zero_index = list(sizes).index(0)
        labels = [l for i, l in enumerate(labels) if i != zero_index]
        sizes = [s for i, s in enumerate(sizes) if i != zero_index]
        colors = [c for i, c in enumerate(colors) if i != zero_index]

    if sizes: # plota o gráfico se houver dados
        ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90,
                textprops={'fontsize': 14, 'fontweight': 'bold'})
    else: 
        ax1.text(0.5, 0.5, "Não há dados de disciplinas.", ha='center', va='center', fontsize=12)

    ax1.set_title('Resumo de Aprovações', fontsize=16, pad=20)

     # Lista de Disciplinas 
    ax2.axis('off') 

    # Formata o texto exibido
    texto_aprovadas = "\n".join(f"• {disciplina}" for disciplina in aprovadas) if aprovadas else "Nenhuma"
    texto_reprovadas = "\n".join(f"• {disciplina}" for disciplina in reprovadas) if reprovadas else "Nenhuma"

    # Posição inicial do texto
    y_pos = 0.95
    
    # Adiciona o texto de aprovadas
    ax2.text(0.0, y_pos, "Aprovadas:", fontsize=14, fontweight='bold', color='mediumseagreen', va='top')
    ax2.text(0.0, y_pos - 0.08, texto_aprovadas, fontsize=12, va='top', ha='left')

    # Adiciona o texto de reprovadas
    ax2.text(0.0, y_pos - 0.45, "Reprovadas:", fontsize=14, fontweight='bold', color='salmon', va='top')
    ax2.text(0.0, y_pos - 0.53, texto_reprovadas, fontsize=12, va='top', ha='left')

    ax2.set_title('Detalhes por Disciplina', fontsize=16, pad=20)

    # Titulo geral da imagem
    fig.suptitle(f'Relatório de Desempenho - Matrícula: {registration}', fontsize=20)

    
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    img_buffer.seek(0)
    plt.close()
    
    return img_buffer

# gera um gráfico de dispersão anônimo comparando a frequência e a 
# média final de todos os alunos para uma disciplina específica
def grafico_frequencia_notas_disciplina(nome_da_disciplina:str):
    caminho_alunos = "datasets/alunos"
    frequencias_dos_alunos = []
    medias_dos_alunos = []

    if not os.path.isdir(caminho_alunos):
        return None
    
    for nome_arquivo in os.listdir(caminho_alunos):
       if nome_arquivo.endswith(".json"):
           caminho_completo = os.path.join(caminho_alunos, nome_arquivo)
           
           try:
               with open(caminho_completo, 'r', encoding='utf-8') as f:
                   student_data = json.load(f)
               
               # Procura pela disciplina especifica nos dados do aluno
               for disciplina_info in student_data:
                   if disciplina_info.get('disciplina') == nome_da_disciplina:
                       freq_str = disciplina_info.get('frequencia_total')
                       media = disciplina_info.get('media_final')
                       
                       # Valida e converte os dados
                       if freq_str and media is not None:
                           frequencia_float = float(freq_str.replace('%', ''))
                           frequencias_dos_alunos.append(frequencia_float)
                           medias_dos_alunos.append(media)
                       # Uma vez que encontrou a disciplina, pode parar de procurar neste aluno
                       break 
           except (json.JSONDecodeError, ValueError, TypeError) as e:
               print(f"Aviso: Ignorando arquivo '{nome_arquivo}' devido a um erro: {e}")
               
    # criando o grafico 

    plt.figure(figsize=(12, 7))
    plt.scatter(frequencias_dos_alunos, medias_dos_alunos, alpha=0.7, label='Alunos (Anônimo)')

    # criando uma linha de tendencia (frequencia afeta a média final?)
    z = np.polyfit(frequencias_dos_alunos, medias_dos_alunos, 1)
    p = np.poly1d(z)
    plt.plot(np.unique(frequencias_dos_alunos), p(np.unique(frequencias_dos_alunos)), "r--", label='Linha de Tendência')

    #estilizando o grafico 
    plt.title(f'Análise de Desempenho em: {nome_da_disciplina}')
    plt.xlabel('Frequência Total (%)')
    plt.ylabel('Média Final')
    plt.xlim(min(frequencias_dos_alunos) - 5, 102)
    plt.ylim(0, 10.5)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()

    # Salva no Buffer
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    return img_buffer





    






                


    


    






