# Backend Class Data

## Ambiente virtual:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

## Instalar dependências:

```bash
pip install -r requirements.txt
```

## Rodar a aplicação

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Rotas
Host: 127.0.0.1:8000

### GET /health

**Descrição:** Testar a atividade do sistema.

### GET /students

**Descrição:** Retorna todos estudantes.

### GET /students/?registration={matricula}

**Descrição:** Retorna informações cadastrais do usuário a partir da matrícula.

### GET /students/{matricula}/frequency

**Descrição:** Retorna a média de frequência do aluno.

### GET /students/{matricula}/frequency/{disciplina}

**Descrição:** Retorna as frequências do aluno na disciplina.

### GET /teacher

**Descrição:** Retorna todos os professores cadastrados.

### GET /teacher?id={id}

**Descrição:** Retorna as informações do professor pelo id.

### GET /classes

**Descrição:** Retorna todas as turmas cadastradas.

### GET /classes?id={id}

**Descrição:** Retorna as informações da turma pelo id.

### GET /grades


### GET /graphics/{registration}/evolucao_das_notas

**Descrição:** Retorna uma imagem de um gráfico de linhas mostrando a evolução das notas de um aluno específico, por bimestre, em todas as suas disciplinas.

### GET /graphics/{registration}/freq_x_media_final

**Descrição:** Retorna uma imagem de um gráfico de dispersão que correlaciona a frequência total com a média final para cada disciplina de um aluno específico.

### GET /graphics/{registration}/status_aprovacao

**Descrição:** Retorna uma imagem de um gráfico de pizza mostrando a proporção de disciplinas aprovadas e reprovadas para um aluno específico.

### GET /graphics/disciplina/{discipline_name}/desempenho_geral

**Descrição:** Retorna uma imagem de um gráfico de dispersão anônimo que correlaciona a frequência com a média final de todos os alunos para uma disciplina específica.

### GET /graphics/disciplinas/ranking_dificuldade

**Descrição:** retorna um gráfico de barras duplo que analisa o desempenho em todas as disciplinas de um curso. O gráfico exibe a média final geral e a taxa de aprovação para cada disciplina, ordenado da mais difícil (menor média) para a mais fácil.

### GET /graphics/disciplina/{discipline_name}/comparativo_professores

**Descrição:** Retorna um gráfico de boxplot que compara a distribuição das médias finais dos alunos em uma disciplina específica, agrupando-os por professor ou turma. Parâmetro de Caminho: {discipline_name},  O nome da disciplina para a qual o comparativo será gerado (ex: "Inteligência Artificial"), no momento só a materia de inteligencia artificial tem 2 turmas. mas é uma função para comparar o desempenho entre dois professores.


