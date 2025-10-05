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

### GET /health
Host: 127.0.0.1:8000

**Descrição:** Testar a atividade do sistema.

### GET /students

**Descrição:** Retorna todos estudantes.

### GET /students/?registration=<matricula> HTTP/1.1

**Descrição:** Retorna informações cadastrais do usuário a partir da matrícula.

### GET /students/<matricula>/frequency

**Descrição:** Retorna a média de frequência do aluno.

### GET /students/<matricula>/frequency/<disciplina>

**Descrição:** Retorna as frequências do aluno na disciplina.

### GET /teacher

**Descrição:** Retorna todos os professores cadastrados.

### GET /teacher?<id>

**Descrição:** Retorna as informações do professor pelo id.

### GET /classes

**Descrição:** Retorna todas as turmas cadastradas.

### GET /classes?<id>

**Descrição:** Retorna as informações da turma pelo id.


### GET /grades