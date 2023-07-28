import warnings

from fastapi import HTTPException, APIRouter
from pydantic import BaseModel, UUID4

warnings.simplefilter(action='ignore', category=FutureWarning)

images_api = APIRouter(prefix='/images', tags=['images'])


# 생성 앨범아트 이미지 가져오기
@images_api.get("/albumart/{user_id}/{image_id}")
async def get_generated_albumart_image(user_id: UUID4, image_id: UUID4):
    return HTTPException(status_code=501, detail="Not implemented (get_generated_albumart_image)")
