from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.services.graphics_services import gerar_grafico_de_linhas

router = APIRouter(prefix="/graphics", tags=["Graphics"])

@router.get("/{registration}/graficos_de_linhas")
def get_grades_bar_chart(registration: str):
    """
    Retorna um gráfico de barras com as médias finais do aluno.
    """
    image_buffer = gerar_grafico_de_linhas(registration)
    
    if image_buffer is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return StreamingResponse(image_buffer, media_type="image/png")
