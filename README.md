# Backend Class Data


## Instalar dependências:

```bash
pip install -r requirements.txt
```

## Rodar a aplicação

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Rotas

### GET /health

**Descrição:** Testar a atividade do sistema.

GET /health HTTP/1.1
Host: 127.0.0.1:8000

### GET /students

**Descrição:** Retorna informações cadastrais do usuário a partir da matrícula.

GET /students/?registration=<matricula> HTTP/1.1
Host: 127.0.0.1:8000

### GET /subjects

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


