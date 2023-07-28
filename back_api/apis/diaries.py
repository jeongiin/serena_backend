import warnings
from uuid import UUID

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel

warnings.simplefilter(action='ignore', category=FutureWarning)

diaries_api = APIRouter(prefix='/diaries', tags=['diaries'])


class Diary(BaseModel):
    user_id: UUID
    title: str
    content: str


@diaries_api.post("/")
async def create_diary(item: Diary):
    return HTTPException(status_code=501, detail="Not implemented")


@diaries_api.get("/")
async def get_diaries(user_id: UUID):
    return HTTPException(status_code=501, detail="Not implemented")