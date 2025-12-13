# Backend Class Data

---

## Ambiente virtual:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```
No Windows

```bash no Windows
.\venv\Scripts\activate    
```


## Instalar dependências:

```bash
pip install -r requirements.txt
```

```bash
sudo apt install uvicorn
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

### GET /teacher?id={id}  ----OK----

**Descrição:** Retorna as informações do professor pelo id.

### GET /teacher/classes?id={teacher_id} ----OK----

**Descrição:** Retorna as turmas que o professor é responsável e os dados das turmas.

**Exemplo de retorno:**
[
    {
        "class_id": "0a93f322-d7ba-43e2-9be1-5d58436177a9",
        "class_name": "TurmaA",
        "teacher_id": "14772494-cd85-44fd-952d-82e4bb4c92a8",
        "students": [
            {
                "student_id": 150035,
                "student_name": "Kevin Lopes",
                "student_uuid": "013d260a-ef56-4de5-8806-2a6173af2106",
                "attendances": [
                { "date": "2025-04-02", "present": true },
                { "date": "2025-04-07", "present": false },
                { "date": "2025-04-09", "present": true },
                { "date": "2025-04-14", "present": true },
                ...
                ],
                "grades": [
                { "evaluation_number": 1, "value": 5.9 },
                { "evaluation_number": 2, "value": 6.8 },
                { "evaluation_number": 3, "value": 8.6 },
                { "evaluation_number": 4, "value": 7.9 }
                ]
            }, ....
        ]
    }
]
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