import warnings

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel, UUID4

warnings.simplefilter(action='ignore', category=FutureWarning)

images_api = APIRouter(prefix='/images', tags=['images'])


# 생성 이미지 가져오기
@images_api.get("/{user_id}/{image_id}")
async def get_generated_image(user_id: UUID4, image_id: UUID4):
    return HTTPException(status_code=501, detail="Not implemented (get_generated_image)")