import warnings
from pydantic import BaseModel
from uuid import UUID

from fastapi import HTTPException, APIRouter

warnings.simplefilter(action='ignore', category=FutureWarning)

diaries_api = APIRouter(prefix='/diaries', tags=['diaries'])


class Diary(BaseModel):
    user_id: UUID
    title: str
    content: str


@diaries_api.post("/")
async def create_diary():
    pass