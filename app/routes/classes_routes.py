from fastapi import APIRouter, HTTPException, Query
from app.services.classes_services import *

router = APIRouter(prefix="/classes",tags=["Classes"])

@router.get("")
def get_classes(
    id: str = Query(None, description="Classes id")
):
    """
    Retorna as turmas cadastradas
    """
    if id:
        infos = get_class_infos(id)
        if not infos:
            raise HTTPException(status_code=404, detail="Teacher not found")
        return infos
    else:
        infos = get_all_classes()
        if not infos:
            raise HTTPException(status_code=404, detail="Teachers not found")
        return infos
