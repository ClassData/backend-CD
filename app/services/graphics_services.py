import os
from io import BytesIO
import matplotlib
matplotlib.use('Agg') # usa um renderizador de alta qualidade sem precisar de uma janela de exibição
import matplotlib.pyplot as plt
import numpy as np
import json
import pandas as pd 
import seaborn as sns
from db_data import supabase


from .students_service import get_student_by_registration

# Garante que o diretório para salvar os gráficos exista
OUTPUT_DIR = "graficos_gerados"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# pegar todas as matriculas 
def get_todas_matriculas():
    try:
        # Busca apenas a coluna 'registration' da tabela 'students'
        response = supabase.table("students").select("registration").execute()
        
        # O banco retorna algo como: [{'registration': '123'}, {'registration': '456'}]
        # Vamos transformar numa lista simples: ['123', '456']
        lista_matriculas = [aluno['registration'] for aluno in response.data]
        
        return lista_matriculas

    except Exception as e:
        print(f"Erro ao buscar matrículas: {e}")
        return []

# Gera um gráfico de barras com a média final de cada disciplina para um aluno. (Atualizado Supabase)
def gerar_grafico_de_linhas(registration: str):
    
    # 1. Converter para string para garantir que o banco entenda
    registration = str(registration)

    try:
        # Descobrir o id do aluno com base na matricula
        response_student = supabase.table("students").select("id").eq("registration", registration).execute()

        if not response_student.data:
            print(f"Aluno não encontrado: {registration}")
            return None
        
        student_id = response_student.data[0]['id']

        # Pegar as notas desse aluno relacionando com a turma (classes) para saber o nome da matéria
        response_grades = supabase.table("grades")\
            .select("value, evaluation_number, classes(name)")\
            .eq("student_id", student_id)\
            .execute()
        
        if not response_grades.data:
            print(f"Aluno {registration} encontrado, mas sem notas lançadas.")
            return None
        
        # Transformar em um dataframe pandas
        df = pd.DataFrame(response_grades.data)
        
        # Extrair o nome da disciplina do objeto aninhado 'classes': {'name': 'Matemática'} -> 'Matemática'
        df['nome_disciplina'] = df['classes'].apply(lambda x: x['name'] if x else 'Desconhecida')

        # Criando o grafico
        plt.figure(figsize=(10, 6))

        # Itera sobre cada disciplina e desenha uma linha
        disciplinas_unicas = df['nome_disciplina'].unique()

        for disciplina in disciplinas_unicas:
            # Filtra apenas as notas dessa matéria
            df_materia = df[df['nome_disciplina'] == disciplina].copy()
            
            # Ordena pelo número da avaliação
            df_materia = df_materia.sort_values(by='evaluation_number')

            if not df_materia.empty:
                plt.plot(
                    df_materia['evaluation_number'], 
                    df_materia['value'], 
                    marker='o', 
                    linestyle='-', 
                    label=disciplina
                )

        plt.title(f"Evolução de Notas - Matrícula: {registration}")  
        plt.ylabel('Nota')
        plt.xlabel('Avaliação (Bimestre/Prova)')
        plt.ylim(0, 10.5)
        plt.grid(True, linestyle='--', alpha=0.7)

        # Ajuste do Eixo X para mostrar apenas números inteiros presentes nos dados
        if not df.empty:
            max_aval = df['evaluation_number'].max()
            plt.xticks(range(1, int(max_aval) + 1))
        
        # Legenda fora do gráfico
        plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        plt.tight_layout(rect=[0, 0, 0.85, 1])

        # Salvar no buffer
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        img_buffer.seek(0)
        plt.close() # Limpa a memória do matplotlib

        return img_buffer

    except Exception as e:
        print(f"Erro ao gerar gráfico: {e}")
        return None


# visualizar a correlação entre a frequencia total e a media final de cada disciplina (Atualizado Supabase)
def gerar_grafico_frequencia_x_notas(registration: str):
    # convertendo tendo a certeza de que é um str 
    registration = str(registration)

    # logica de pegar os dados e analisar eles 
    resp_aluno = supabase.table("students").select("id").eq("registration", registration).execute()
    if not resp_aluno.data:
      print("Aluno não encontrado")
      return None 
    student_id = resp_aluno.data[0]["id"]

    grades_data = supabase.table("grades")\
    .select("value, classes(id, name, subjects(name))")\
    .eq("student_id", student_id)\
    .execute()

    # busca as presenças 
    attendance_data = supabase.table("attendance")\
    .select("present, classes(id)")\
    .eq("student_id", student_id)\
    .execute()

    # se não tiver nenhum dos dois dados 
    if not grades_data.data or not attendance_data.data:
        print("Dados insuficientes de notas ou presença para gerar gráfico.")
        return None
    
    # Processamento dos dados 
    # Calcular Média das Notas por Turma
    df_notas = pd.DataFrame(grades_data.data)
    # Extrai ID e Nome da disciplina do JSON aninhado
    df_notas['class_id'] = df_notas['classes'].apply(lambda x: x['id'])

    #pequena função para pegar o nome das turmas (o materia)

    def get_label_name(row):
      materia = row['classes']['subjects']['name'] if row['classes']['subjects'] else 'Desconhecida'
      turma = row['classes']['name'] # Ex: "PDS1 - TuRMA a"
    
      # Retorna algo como: "PDS I ( turma B)"
      return f"{materia} ({turma})"



    df_notas['disciplina_label'] = df_notas.apply(lambda row: get_label_name(row), axis=1)
    # Agrupa por turma e tira a média das notas
    df_medias = df_notas.groupby(['class_id', 'disciplina_label'])['value'].mean().reset_index(name='media_final')


    #Calcular Frequência por Turma
    df_freq = pd.DataFrame(attendance_data.data)
    df_freq['class_id'] = df_freq['classes'].apply(lambda x: x['id'])
        
    # Agrupa por turma:
    df_calculo_freq = df_freq.groupby('class_id')['present'].agg(['sum', 'count']).reset_index()
        
    # Fórmula: (Presenças / Total Aulas) * 100
    df_calculo_freq['frequencia_total'] = (df_calculo_freq['sum'] / df_calculo_freq['count']) * 100

    # Juntar as duas tabelas (Cruzamento via class_id)
    # O 'inner' garante que só pegamos matérias que têm TANTO notas QUANTO chamadas lançadas
    df_final = pd.merge(df_medias, df_calculo_freq[['class_id', 'frequencia_total']], on='class_id', how='inner')

    if df_final.empty:
        return None
    
    # Gerando o grafico
    frequencias = df_final['frequencia_total'].tolist()
    media_finais = df_final['media_final'].tolist()
    nomes_das_disciplinas = df_final['disciplina_label'].tolist()

    plt.figure(figsize=(10, 6))

    plt.scatter(frequencias, media_finais, color='dodgerblue', alpha=0.7, s=100) # s=100 aumenta o tamanho da bolinha

    for i, txt in enumerate(nomes_das_disciplinas):
            plt.annotate(
                txt, 
                (frequencias[i], media_finais[i]), 
                textcoords="offset points", 
                xytext=(0, 8), 
                ha='center', 
                fontsize=9,
                fontweight='bold'
            )

    plt.title(f'Relação Frequência vs. Nota Final - Matrícula {registration}')
    plt.xlabel('Frequência Total (%)')
    plt.ylabel('Média Final')

    # Ajustes visuais
    plt.xlim(min(frequencias) - 5 if frequencias else 0, 105) 
    plt.ylim(0, 10.5) 
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Salva no buffer
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()



    return img_buffer

# grafico de pizza (Atualizado Supabase)
def status_de_aprovação_pizza(registration: str):
    registration = str(registration)

    # # regras de aprovação 
    nota_minima = 7.0 
    freq_min = 75.0 

    
    # Pega ID do aluno
    resp_aluno = supabase.table("students").select("id").eq("registration", registration).execute()
    if not resp_aluno.data:
        return None
    student_id = resp_aluno.data[0]['id']
    # Pega Notas e Presenças
    # Precisamos do 'subjects(name)' para saber o nome da matéria na lista
    grades_data = supabase.table("grades").select("value, classes(id, name, subjects(name))").eq("student_id", student_id).execute()
    attendance_data = supabase.table("attendance").select("present, classes(id)").eq("student_id", student_id).execute()
    if not grades_data.data or not attendance_data.data:
        print("Dados insuficientes para calcular aprovação.")
        return None
    
    # Calculo e ordenação dos dados 
    #Calcular Médias
    df_notas = pd.DataFrame(grades_data.data)
    df_notas['class_id'] = df_notas['classes'].apply(lambda x: x['id'])
    
    # Pega o nome da matéria (ou da turma se não tiver matéria)
    def get_subject_name(class_obj):
        if class_obj and 'subjects' in class_obj and class_obj['subjects']:
            return class_obj['subjects']['name']
        return class_obj.get('name', 'Desconhecida')
    df_notas['disciplina'] = df_notas['classes'].apply(get_subject_name)
    
    # Agrupa e calcula média final
    df_medias = df_notas.groupby(['class_id', 'disciplina'])['value'].mean().reset_index(name='media_final')
    # Calcular Frequência
    df_freq = pd.DataFrame(attendance_data.data)
    df_freq['class_id'] = df_freq['classes'].apply(lambda x: x['id'])
    
    df_calculo_freq = df_freq.groupby('class_id')['present'].agg(['sum', 'count']).reset_index()
    df_calculo_freq['frequencia_total'] = (df_calculo_freq['sum'] / df_calculo_freq['count']) * 100
    # Juntar tudo 
    df_final = pd.merge(df_medias, df_calculo_freq[['class_id', 'frequencia_total']], on='class_id', how='inner')
    if df_final.empty:
        return None
    
    # regras de aprovação 
    def verificar_status(row):
        if row['media_final'] >= nota_minima and row['frequencia_total'] >= freq_min:
            return 'Aprovado'
        else:
            return 'Reprovado'
        
    df_final['status_aprovacao'] = df_final.apply(verificar_status, axis=1)
    # fazendo o grafico 
    contagem = df_final['status_aprovacao'].value_counts()
    aprovados_count = contagem.get('Aprovado', 0)
    reprovados_count = contagem.get('Reprovado', 0)
    # Listas de nomes para o texto lateral
    lista_aprovadas = df_final[df_final['status_aprovacao'] == 'Aprovado']['disciplina'].tolist()
    lista_reprovadas = df_final[df_final['status_aprovacao'] == 'Reprovado']['disciplina'].tolist()
    # plotando 
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), gridspec_kw={'width_ratios': [1.2, 1]}) 

    # Dados da pizza
    labels = ['Aprovado', 'Reprovado']
    sizes = [aprovados_count, reprovados_count]
    colors = ['green', 'red'] # Cores fixas para manter padrão

    # Remove fatias zeradas para não ficar feio
    dados_filtrados = [(s, l, c) for s, l, c in zip(sizes, labels, colors) if s > 0]
    if dados_filtrados:
        sizes_f, labels_f, colors_f = zip(*dados_filtrados)
        ax1.pie(sizes_f, labels=labels_f, colors=colors_f, autopct='%1.1f%%', startangle=90,
                textprops={'fontsize': 14, 'fontweight': 'bold'})
    else:
        ax1.text(0.5, 0.5, "Sem dados suficientes", ha='center', va='center')
    ax1.set_title('Resumo de Aprovações', fontsize=16, pad=20)
    # Parte do Texto (Lateral)
    ax2.axis('off')
    
    texto_aprovadas = "\n".join(f"• {disc}" for disc in lista_aprovadas) if lista_aprovadas else "Nenhuma"
    texto_reprovadas = "\n".join(f"• {disc}" for disc in lista_reprovadas) if lista_reprovadas else "Nenhuma"
    y_pos = 0.95
    
    # Bloco Aprovadas
    ax2.text(0.0, y_pos, f"Aprovadas ({len(lista_aprovadas)}):", fontsize=14, fontweight='bold', color='mediumseagreen', va='top')
    ax2.text(0.0, y_pos - 0.08, texto_aprovadas, fontsize=12, va='top', ha='left')

    
    # Ajustei o espaçamento vertical dinamicamente para não sobrepor se a lista de cima for grande
    espaco_lista_1 = 0.10 + (len(lista_aprovadas) * 0.05)
    y_pos_reprovadas = y_pos - espaco_lista_1
    
    ax2.text(0.0, y_pos_reprovadas, f"Reprovadas ({len(lista_reprovadas)}):", fontsize=14, fontweight='bold', color='salmon', va='top')
    ax2.text(0.0, y_pos_reprovadas - 0.08, texto_reprovadas, fontsize=12, va='top', ha='left')
    ax2.set_title('Detalhes por Disciplina', fontsize=16, pad=20)
    fig.suptitle(f'Relatório de Desempenho - Matrícula: {registration}', fontsize=20)

    # Salvar
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png', bbox_inches='tight')
    img_buffer.seek(0)
    plt.close()

    return img_buffer
    


# gera um gráfico de dispersão anônimo comparando a frequência e a média final de todos os alunos para uma disciplina específica (Atualizado SUPABSE)
def grafico_frequencia_notas_disciplina(nome_da_disciplina: str):
    
    # Busca a disciplina pelo nome para pegar o ID dela
    # E já aproveita para pegar os IDs das turmas vinculadas a ela
    resp_subject = supabase.table("subjects")\
        .select("id, classes(id)")\
        .eq("name", nome_da_disciplina)\
        .execute()
    if not resp_subject.data:
        print(f"Disciplina '{nome_da_disciplina}' não encontrada.")
        return None
    # Lista de IDs das turmas dessa matéria
    turmas_ids = [t['id'] for t in resp_subject.data[0]['classes']]
    
    if not turmas_ids:
        print(f"A disciplina '{nome_da_disciplina}' não tem turmas cadastradas.")
        return None
    
    # Busca TODAS as notas dessas turmas
    # .in_() serve para buscar "onde class_id esteja NA lista X"
    grades_data = supabase.table("grades")\
        .select("student_id, value, class_id")\
        .in_("class_id", turmas_ids)\
        .execute()
    
    # Busca TODAS as presenças dessas turmas
    attendance_data = supabase.table("attendance")\
        .select("student_id, present, class_id")\
        .in_("class_id", turmas_ids)\
        .execute()
    
    if not grades_data.data or not attendance_data.data:
        print("Dados insuficientes de notas ou frequência.")
        return None
    # Preparando os dados 
    
    # Calcular Média Final de cada aluno nessas turmas
    df_notas = pd.DataFrame(grades_data.data)

    # Agrupa por aluno e calcula a média das notas dele
    df_medias = df_notas.groupby('student_id')['value'].mean().reset_index(name='media_final')

    # Calcular Frequência de cada aluno
    df_freq = pd.DataFrame(attendance_data.data)

    # Agrupa por aluno: Soma os 'True' (presenças) e conta o total de registros
    df_calculo_freq = df_freq.groupby('student_id')['present'].agg(['sum', 'count']).reset_index()
    df_calculo_freq['frequencia_total'] = (df_calculo_freq['sum'] / df_calculo_freq['count']) * 100

    # CJuntar as duas informações 
    df_final = pd.merge(df_medias, df_calculo_freq[['student_id', 'frequencia_total']], on='student_id', how='inner')
    if df_final.empty:
        return None
    
    # Extraindo listas para o plot
    frequencias_dos_alunos = df_final['frequencia_total']
    medias_dos_alunos = df_final['media_final']

    # Gerando o grafico 
    plt.figure(figsize=(12, 7))
    plt.scatter(frequencias_dos_alunos, medias_dos_alunos, alpha=0.7, label='Alunos (Anônimo)', color='royalblue')

    # Lógica da Linha de Tendência 
    # Só gera se tiver mais de 1 ponto, senão dá erro matemático
    if len(frequencias_dos_alunos) > 1:
        z = np.polyfit(frequencias_dos_alunos, medias_dos_alunos, 1)
        p = np.poly1d(z)
        
        # Cria pontos para a linha vermelha
        plt.plot(
            np.unique(frequencias_dos_alunos), 
            p(np.unique(frequencias_dos_alunos)), 
            "r--", 
            label=f'Tendência (y={z[0]:.2f}x + {z[1]:.2f})'
        )
    # Estilizando
    plt.title(f'Análise de Desempenho em: {nome_da_disciplina}')
    plt.xlabel('Frequência Total (%)')
    plt.ylabel('Média Final')
    
    # Ajuste de Limites
    plt.xlim(min(frequencias_dos_alunos) - 5, 105) # Um pouco de margem
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



# função necessarias para graficos mais complexos (Atualizado supabase)
def carregar_dados_todos_alunos():
    """
    Busca dados de TODOS os alunos, calcula médias e frequências por disciplina
    e retorna um DataFrame consolidado.
    """
    # pegando os dados 
    response_grades = supabase.table("grades")\
      .select("value, student_id, students(name, registration), classes(id, name, subjects(name))")\
      .execute()
    
    # Buscar TODAS as Presenças
    response_attendance = supabase.table("attendance")\
        .select("present, student_id, class_id")\
        .execute()
    
    if not response_grades.data or not response_attendance.data:
            print(" Dados insuficientes no banco.")
            return pd.DataFrame()
    
    # processando os dados 
    df_grades = pd.DataFrame(response_grades.data) 
    # Extrair dados aninhados 
    # aluno
    df_grades['username_aluno'] = df_grades['students'].apply(lambda x: x['name']) # Usando nome como username
    df_grades['registration'] = df_grades['students'].apply(lambda x: x['registration'])
    
    # turma/materia
    df_grades['class_id'] = df_grades['classes'].apply(lambda x: x['id'])
    df_grades['turma'] = df_grades['classes'].apply(lambda x: x['name'])

    # pegar o nome das disciplinas
    def get_disciplina(x):
        if x and 'subjects' in x and x['subjects']:
            return x['subjects']['name']
        return x.get('name', 'Desconhecida')
        
    df_grades['disciplina'] = df_grades['classes'].apply(get_disciplina)
    # Calcular MÉDIA FINAL por Aluno e Turma

    df_medias = df_grades.groupby(['student_id', 'username_aluno', 'registration', 'class_id', 'disciplina', 'turma'])['value'].mean().reset_index(name='media_final')
    # Preparar DataFrame de Presença

    df_att = pd.DataFrame(response_attendance.data)
    
    # Calcular FREQUÊNCIA por Aluno e Turma
    df_freq_calc = df_att.groupby(['student_id', 'class_id'])['present'].agg(['sum', 'count']).reset_index()
     
    # Fórmula: (Presenças / Total) * 100
    df_freq_calc['frequencia_total'] = (df_freq_calc['sum'] / df_freq_calc['count']) * 100
   
    # Juntamos as médias com as frequências usando ID do Aluno e ID da Turma
    df_final = pd.merge(df_medias, df_freq_calc[['student_id', 'class_id', 'frequencia_total']], 
                        on=['student_id', 'class_id'], 
                        how='inner')
    print(f" Dados carregados: {len(df_final)} registros processados.")
    
    # Retorna o DataFrame limpo com as colunas essenciais
    return df_final[['username_aluno', 'registration', 'disciplina', 'media_final', 'frequencia_total', 'turma']]



# ex: http://127.0.0.1:8000/graphics/disciplinas/ranking_dificuldade (Atualizado supabase)
def gerar_ranking_dificuldade_disciplinas():
    """
    Gera um gráfico de barras horizontal mostrando a média final e a taxa de aprovação
    para cada disciplina, ordenado da mais difícil para a mais fácil.
    """
    # Carregar dados do Supabase (já vem como DataFrame limpo)
    df_alunos = carregar_dados_todos_alunos()
    
    if df_alunos.empty:
        return None
    
    # Como o banco não salva "Aprovado", calculamos agora:
    MEDIA_MINIMA = 7.0
    FREQ_MINIMA = 75.0

    # Cria coluna binária: 1 se passou, 0 se reprovou
    df_alunos['aprovado_bin'] = (
        (df_alunos['media_final'] >= MEDIA_MINIMA) & 
        (df_alunos['frequencia_total'] >= FREQ_MINIMA)
    ).astype(int)

    # Agregando os dados por disciplin
    df_disciplinas = df_alunos.groupby('disciplina').agg(
        media_final_geral=('media_final', 'mean'),
        taxa_aprovacao_geral=('aprovado_bin', 'mean'),
        frequencia_media_geral=('frequencia_total', 'mean')
    ).reset_index()

    # Multiplica a taxa de aprovação por 100 para ficar em % (0.9 -> 90.0)
    df_disciplinas['taxa_aprovacao_geral'] *= 100
    
    # Ordena pela média final (da menor para a maior -> Mais difíceis no topo se usar barplot horizontal)
    df_disciplinas = df_disciplinas.sort_values(by='media_final_geral', ascending=True)

    #  PLOTAGEM 
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 10))
    fig.suptitle('Análise de Dificuldade das Disciplinas', fontsize=20)

    # Gráfico Média Final
    sns.barplot(x='media_final_geral', y='disciplina', data=df_disciplinas, ax=ax1, color='salmon')
    ax1.set_title('Média Final Geral por Disciplina')
    ax1.set_xlabel('Média Final (0-10)')
    ax1.set_ylabel('Disciplina')
    ax1.set_xlim(0, 10)
    
    # Adiciona os valores nas barras
    for p in ax1.patches:
        # Verifica se a largura é maior que 0 para evitar erros em barras vazias
        width = p.get_width()
        if width > 0:
            ax1.annotate(f"{width:.1f}", 
                         (width + 0.1, p.get_y() + p.get_height() / 2),
                         va='center')

    # Gráfico Taxa de Aprovação
    sns.barplot(x='taxa_aprovacao_geral', y='disciplina', data=df_disciplinas, ax=ax2, color='mediumseagreen')
    ax2.set_title('Taxa de Aprovação Geral por Disciplina')
    ax2.set_xlabel('Taxa de Aprovação (%)')
    ax2.set_ylabel('') # Remove label Y duplicado
    ax2.set_xlim(0, 105) # Um pouco mais de espaço para o texto
    
    # Adiciona os valores nas barras
    for p in ax2.patches:
        width = p.get_width()
        if width > 0:
            ax2.annotate(f"{width:.1f}%", 
                         (width + 1, p.get_y() + p.get_height() / 2),
                         va='center')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Salva no buffer
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()

    return img_buffer


def gerar_comparativo_desempenho_professor(nome_da_disciplina: str): # (Atualizado SuPABASE)
    """
    Gera um boxplot comparando a distribuição das médias finais entre
    professores de mesma disciplina, buscando dados direto do Supabase.
    """
    #Pegar os dados da disciplina 
    resp_subject = supabase.table("subjects").select("id").eq("name", nome_da_disciplina).execute()
    if not resp_subject.data:
        print(f"Disciplina '{nome_da_disciplina}' não encontrada.")
        return None
    subject_id = resp_subject.data[0]['id']

    # pegar as turmas dessas disciplinas e e seus professores 
    resp_classes = supabase.table("classes")\
            .select("id, classes_teachers(teachers(name))")\
            .eq("subject_id", subject_id)\
            .execute()
    
    if not resp_classes.data:
            print("Nenhuma turma encontrada para essa disciplina.")
            return None
    
    # criar uma lista e uma biblioteca para professores e turmas
    mapa_professores = {}
    turmas_ids = []

    for turma in resp_classes.data:
        turma_id = turma['id']
        turmas_ids.append(turma_id)
            
        # Extrai nomes dos professores da estrutura aninhada
        lista_profs = []
        if turma['classes_teachers']:
            for item in turma['classes_teachers']:
                if item['teachers']:
                    lista_profs.append(item['teachers']['name'])
        
        # Se tiver professores, junta os nomes. Se não, chama de "Sem Professor"
        nome_final = ", ".join(lista_profs) if lista_profs else "Não Atribuído"
        mapa_professores[turma_id] = nome_final

        #Buscando as notas 
        resp_grades = supabase.table("grades")\
            .select("value, class_id")\
            .in_("class_id", turmas_ids)\
            .execute()
        
        # Montar o DataFrame Final
        df_notas = pd.DataFrame(resp_grades.data)

        # Adiciona o nome do professor baseado no ID da turma (Map)
        df_notas['nome_professor'] = df_notas['class_id'].map(mapa_professores)
        
        # Renomeia para facilitar o plot (para ficar igual ao seu código original)
        df_notas = df_notas.rename(columns={'value': 'media_final'})

        # Verificação mínima para gerar gráfico
        if df_notas.empty or df_notas['nome_professor'].nunique() < 2:
            print("Dados insuficientes para comparação (precisa de pelo menos 2 professores/turmas distintas).")
            #  Retornar gráfico mesmo com 1 professor, se quiser, remova a condição acima.
            if df_notas['nome_professor'].nunique() == 0:
                return None
            
    # PLOTAGEM 
    plt.figure(figsize=(10, 7))
    
    # Boxplot
    sns.boxplot(x='nome_professor', y='media_final', data=df_notas, palette='pastel', hue='nome_professor', legend=False)
    
    # Stripplot (pontinhos pretos)
    sns.stripplot(x='nome_professor', y='media_final', data=df_notas, color='black', alpha=0.5, jitter=0.1)
    plt.title(f'Comparativo de Desempenho em: {nome_da_disciplina}')
    plt.xlabel('Professor(es) da Turma')
    plt.ylabel('Média Final dos Alunos')
    plt.ylim(0, 10.5)
    plt.grid(True, linestyle='--', alpha=0.6, axis='y')
    plt.tight_layout()
    
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    plt.close()
    return img_buffer








    






                


    


    






