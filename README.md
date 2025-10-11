# Backend Class Data

---

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

---

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

---


