import os
from io import BytesIO
import matplotlib
matplotlib.use('Agg') # usa um renderizador de alta qualidade sem precisar de uma janela de exibição
import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd
import seaborn as sns 

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

# Fazendo graficos mais complexos.

def carregar_dados_todos_alunos(caminho_pasta_alunos="datasets/alunos"):
    """
    Lê todos os arquivos JSON da pasta de alunos e os consolida em um DataFrame pandas.
    """
    dados_completos = []
    
    if not os.path.isdir(caminho_pasta_alunos):
        print(f"Erro: Diretório não encontrado '{caminho_pasta_alunos}'")
        return pd.DataFrame() # Retorna DataFrame vazio

    for nome_arquivo in os.listdir(caminho_pasta_alunos):
        if nome_arquivo.endswith(".json"):
            # Extrai o "username" do aluno a partir do nome do arquivo
            # Ex: "arthur_rodrigues_435678.json" -> "arthur_rodrigues"
            partes_nome = nome_arquivo.split('_')
            username_aluno = f"{partes_nome[0]}_{partes_nome[1]}"
            
            caminho_completo = os.path.join(caminho_pasta_alunos, nome_arquivo)
            try:
                with open(caminho_completo, 'r', encoding='utf-8') as f:
                    dados_aluno = json.load(f)
                    # Adiciona o username a cada registro de disciplina
                    for disciplina in dados_aluno:
                        disciplina['username_aluno'] = username_aluno
                        dados_completos.append(disciplina)
            except Exception as e:
                print(f"Erro ao ler o arquivo {nome_arquivo}: {e}")
                
    return pd.DataFrame(dados_completos)

# agora vamos fazer um rankingh de dificuladade das disciplinas 

# ex: http://127.0.0.1:8000/graphics/disciplinas/ranking_dificuldade
def gerar_ranking_dificuldade_disciplinas():
    """
    Gera um gráfico de barras horizontal mostrando a média final e a taxa de aprovação
    para cada disciplina, ordenado da mais difícil para a mais fácil.
    """
    # Carregar e processar os dados
    df_alunos = carregar_dados_todos_alunos()
    if df_alunos.empty:
        return None
    
    # Converte 'frequencia_total' para numérico (ex: "91.2%" -> 91.2)
    df_alunos['frequencia_num'] = df_alunos['frequencia_total'].str.replace('%', '').astype(float)
    # Converte 'status_aprovacao' para binário (Aprovado=1, Reprovado=0)
    df_alunos['aprovado_bin'] = (df_alunos['status_aprovacao'] == 'Aprovado').astype(int)

    #  Agregando os dados por disciplina
    df_disciplinas = df_alunos.groupby('disciplina').agg(
        media_final_geral=('media_final', 'mean'),
        taxa_aprovacao_geral=('aprovado_bin', 'mean'),
        frequencia_media_geral=('frequencia_num', 'mean')
    ).reset_index()

    # Multiplica a taxa de aprovação por 100 para visualização
    df_disciplinas['taxa_aprovacao_geral'] *= 100
    
    # Ordena pela média final (da menor para a maior)
    df_disciplinas = df_disciplinas.sort_values(by='media_final_geral', ascending=True)

    # Criar o gráfico (dois subplots lado a lado)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))
    fig.suptitle('Análise de Dificuldade das Disciplinas', fontsize=20)

    # Gráfico 1: Média Final
    sns.barplot(x='media_final_geral', y='disciplina', data=df_disciplinas, ax=ax1, color='salmon')
    ax1.set_title('Média Final Geral por Disciplina')
    ax1.set_xlabel('Média Final (0-10)')
    ax1.set_ylabel('Disciplina')
    ax1.set_xlim(0, 10)
    # Adiciona os valores nas barras
    for p in ax1.patches:
        ax1.annotate(f"{p.get_width():.1f}", (p.get_width() + 0.1, p.get_y() + p.get_height() / 2),
                     va='center')

    # Gráfico 2: Taxa de Aprovação
    sns.barplot(x='taxa_aprovacao_geral', y='disciplina', data=df_disciplinas, ax=ax2, color='mediumseagreen')
    ax2.set_title('Taxa de Aprovação Geral por Disciplina')
    ax2.set_xlabel('Taxa de Aprovação (%)')
    ax2.set_ylabel('') # Remove o label Y duplicado
    ax2.set_xlim(0, 100)
    # Adiciona os valores nas barras
    for p in ax2.patches:
        ax2.annotate(f"{p.get_width():.1f}%", (p.get_width() + 1, p.get_y() + p.get_height() / 2),
                     va='center')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95]) # Ajusta para o supertítulo

    # Salva no buffer
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    return img_buffer


# vamos tentar algo que conecte os 3 jsons 

# comparativo de desempenho por professor 

def gerar_comparativo_desempenho_professor(nome_da_disciplina: str):
    """
    Gera um boxplot comparando a distribuição das médias finais entre
    professores de mesma disciplina.
    """
    # Carregar dados das turmas 
    try:
        df_turmas = pd.read_json("datasets/turmas.json")
    except Exception as e:
        print(f"Erro ao ler turmas.json: {e}")
        return None
        
    # Carregar dados de todos os alunos (usando a função que criamos)
    df_alunos = carregar_dados_todos_alunos()
    if df_alunos.empty:
        return None

    # 3 Filtrar os dados APENAS para a disciplina de interesse
    df_turmas_disciplina = df_turmas[df_turmas['disciplina'] == nome_da_disciplina].copy()
    df_alunos_disciplina = df_alunos[df_alunos['disciplina'] == nome_da_disciplina].copy()

    if df_turmas_disciplina.empty or df_alunos_disciplina.empty:
        return None 

    
    # A lista de professores pode ter múltiplos nomes, então convertemos para string
    # Ex: ["Ricardo Almeida", "Vanessa Campos"] -> "Ricardo Almeida, Vanessa Campos"
    df_turmas_disciplina['nome_professor'] = df_turmas_disciplina['professor(es)'].apply(lambda x: ", ".join(x))
    
    # "Explode" a lista de alunos: cria uma linha para cada aluno na turma
    df_mapeamento = df_turmas_disciplina.explode('alunos')
    
    # Renomeia a coluna 'alunos' para 'username_aluno' para o merge
    df_mapeamento = df_mapeamento.rename(columns={'alunos': 'username_aluno'})
    
    # Junta os dados dos alunos (com as notas) com os dados das turmas (com os professores)
    df_final = pd.merge(
        df_alunos_disciplina,
        df_mapeamento[['username_aluno', 'nome_professor']],
        on='username_aluno',
        how='inner' # Só mantém alunos que estão em uma turma
    )

    if df_final.empty or df_final['nome_professor'].nunique() < 2:
        # Não é possível comparar se não houver dados ou se houver apenas 1 professor
        return None

    # 5. Gerar o Gráfico (Boxplot)
    plt.figure(figsize=(10, 7))
    sns.boxplot(x='nome_professor', y='media_final', data=df_final, palette='pastel', hue='nome_professor' , legend=False)
    
    # Adiciona os pontos de dados (alunos) sobre o boxplot para mais detalhes
    sns.stripplot(x='nome_professor', y='media_final', data=df_final, color='black', alpha=0.5, jitter=0.1)

    plt.title(f'Comparativo de Desempenho em: {nome_da_disciplina}')
    plt.xlabel('Professor(es) da Turma')
    plt.ylabel('Média Final dos Alunos')
    plt.ylim(0, 10.5)
    plt.grid(True, linestyle='--', alpha=0.6, axis='y')
    plt.tight_layout()
    
    # Salva no buffer
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    return img_buffer









    






                


    


    






