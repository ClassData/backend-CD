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

### GET /grades