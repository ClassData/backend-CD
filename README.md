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

### GET /health         ----OK----

**Descrição:** Testar a atividade do sistema.

--- 

## Dados de Estudantes

### GET /students       ----OK----

**Descrição:** Retorna todos estudantes.

### GET /students/?registration={matricula} ----OK----

**Descrição:** Retorna informações cadastrais do usuário a partir da matrícula.

<!-- ### GET /students/{matricula}/frequency   

**Descrição:** Retorna a média de frequência do aluno em todas as . -->

**Descrição:** Retorna as turmas que o professor é responsável.

### GET /students/{registration}/frequency/{class_id}  ----OK----

**Descrição:** Retorna as frequências do aluno na disciplina.
**Exemplo de retorno:**
{
    "registration":"150000","subject_id":"021be5c0-ce0e-4515-b3ab-b047e1058cce",
    "total_aulas":72,
    "aulas_presente":67,
    "frequencia":93.06
}

--- 

## Dados de Professores

### GET /teacher          ----OK----

**Descrição:** Retorna todos os professores cadastrados.

### GET /teacher?id={id} ----OK----

**Descrição:** Retorna as informações do professor pelo id.

### GET /teacher?id={id}/classes

**Descrição:** Retorna as turmas que o professor é responsável.

--- 

## Dados de Turmas 

### GET /classes         ----OK----

**Descrição:** Retorna todas as turmas cadastradas.

### GET /classes?id={id} ----OK----

**Descrição:** Retorna as informações da turma pelo id.

--- 

## Notas dos alunos

### GET /grades/{registration}/{class_id}
**Descrição:** Retorna as informações da turma pelo id.
**Exemplo de retorno:**
{
    "registration":"150000","subject_id":"021be5c0-ce0e-4515-b3ab-b047e1058cce",
    "total_aulas":72,
    "aulas_presente":67,
    "frequencia":93.06
}

### GET /graphics/{registration}/evolucao_das_notas

**Descrição:** Retorna uma imagem de um gráfico de linhas mostrando a evolução das notas de um aluno específico, por bimestre, em todas as suas disciplinas.

### GET /graphics/{registration}/freq_x_media_final

**Descrição:** Retorna uma imagem de um gráfico de dispersão que correlaciona a frequência total com a média final para cada disciplina de um aluno específico.

### GET /graphics/{registration}/status_aprovacao

**Descrição:** Retorna uma imagem de um gráfico de pizza mostrando a proporção de disciplinas aprovadas e reprovadas para um aluno específico.

### GET /graphics/disciplina/{discipline_name}/desempenho_geral

**Descrição:** Retorna uma imagem de um gráfico de dispersão anônimo que correlaciona a frequência com a média final de todos os alunos para uma disciplina específica.

---