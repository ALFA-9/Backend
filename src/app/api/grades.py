from typing import List

from app.api import crud
from app.api.models import GradeDB, GradeSchema
from fastapi import APIRouter, HTTPException, Path
from typing_extensions import Annotated

router = APIRouter()


# Как вьюшки или функции в Django
@router.get('/', response_model=List[GradeDB])
async def get_all_grades():
    return await crud.get_all_grades()


@router.post("/", response_model=GradeDB, status_code=201)
async def create_grade(payload: GradeSchema):
    grade_id = await crud.post_grade(payload)
    response_object = {
        "id": grade_id,
        "title": payload.title,
    }
    return response_object


@router.get("/{id}/", response_model=GradeDB)
# Id аннатируем с валидацией (в данном случае >=0)
async def get_grade(id: Annotated[int, Path(..., gt=0)],):
    grade = await crud.get_grade(id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade
