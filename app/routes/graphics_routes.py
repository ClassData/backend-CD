from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.services.graphics_services import *

router = APIRouter(prefix="/graphics", tags=["Graphics"])


# ex: http://127.0.0.1:8000/graphics/144335/evolucao_das_notas
@router.get("/{registration}/evolucao_das_notas")
def get_grades_bar_chart(registration: str):
    """
    Retorna um gráfico de barras com as médias finais do aluno.
    """
    image_buffer = gerar_grafico_de_linhas(registration)
    
    if image_buffer is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return StreamingResponse(image_buffer, media_type="image/png")

# ex: http://127.0.0.1:8000/graphics/144335/freq_x_media_final
@router.get("/{registration}/freq_x_media_final")
def get_grafico_freq_x_mediaf(registration: str):
      """
    Retorna um gráfico com a relaçao de frequencia e media final de um aluno em cada disciplina
    """
      image_buffer =  gerar_grafico_frequencia_x_notas(registration)

      if image_buffer is None:
           raise HTTPException(status_code=404, detail="Student not found")
      return StreamingResponse(image_buffer, media_type="image/png")

# ex: http://127.0.0.1:8000/graphics/144335/status_aprovacao
@router.get("/{registration}/status_aprovacao")
def get_approval_status_pie_chart(registration: str):
    """
    Retorna um gráfico de pizza com a proporção de aprovações e reprovações.
    """
    image_buffer = status_de_aprovação_pizza(registration)
    
    if image_buffer is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return StreamingResponse(image_buffer, media_type="image/png")

# ex: http://127.0.0.1:8000/graphics/disciplina/Redes%20de%20Computadores/desempenho_geral
@router.get("/disciplina/{discipline_name}/desempenho_geral")
def get_grafico_de_disciplina_nota_x_freq(discipline_name: str):
    """
    Retorna um gráfico de dispersão anônimo com a relação entre
    frequência e média final de todos os alunos em uma disciplina.
    """
    image_buffer = grafico_frequencia_notas_disciplina(discipline_name)
    
    if image_buffer is None:
        raise HTTPException(status_code=404, detail="discipline not found")

    return StreamingResponse(image_buffer, media_type="image/png")
      

           

