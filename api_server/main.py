import os
import warnings

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, JSONResponse

try:
    from .apis import MeloDB, diaries, letters, chats, models, common
except ImportError:
    from apis import MeloDB, diaries, letters, chats, models, common

warnings.simplefilter(action='ignore', category=FutureWarning)

app = FastAPI(title="SKT FLY AI Melovision Internal API Service",
              redoc_url=None)
app.include_router(common.common_api)
# app.include_router(diaries.diaries_api)
# app.include_router(letters.letters_api)
# app.include_router(chats.chats_api)
app.include_router(models.models_api)

AUTH_KEY = os.environ.get('AUTH_KEY')

MUSIC_OUTPUTS_PATH = os.path.join(os.path.dirname(__file__), 'music_outputs')
MUSIC_THUMBNAILS_PATH = os.path.join(os.path.dirname(__file__), 'music_thumbnails')

MeloDB = MeloDB()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    print(exc.errors())
    print(exc.body)
    return PlainTextResponse(status_code=422, content=f"detail: {exc.errors()}\nbody: {exc.body}")


@app.get("/")
async def root():
    return {"message": "SKT FLY AI Melovision Internal API Service"}


@app.delete("/management/outputs")
async def delete_outputs(auth: str):
    """
    # DB 관리용 엔드포인트
    # 사용하지 않는 음악 파일 삭제
    # 사용하지 않는 썸네일 파일 삭제
    """
    removed_music_ids = []
    removed_thumbnail_ids = []

    if auth == AUTH_KEY:
        music = MeloDB.melo_music.find({})
        for m in music:
            music_id = str(m['_id'])

            if os.path.exists(os.path.join(MUSIC_OUTPUTS_PATH, music_id + '.wav')):
                pass
            else:
                print('remove', music_id + '.wav')
                removed_music_ids.append(music_id)
                os.remove(os.path.join(MUSIC_OUTPUTS_PATH, music_id + '.wav'))

            if os.path.exists(os.path.join(MUSIC_THUMBNAILS_PATH, music_id + '.jpg')):
                pass
            else:
                print('remove', music_id + '.jpg')
                removed_thumbnail_ids.append(music_id)
                os.remove(os.path.join(MUSIC_THUMBNAILS_PATH, music_id + '.jpg'))

    else:
        return JSONResponse(status_code=401, content={"detail": "Invalid auth key"})

    return JSONResponse(status_code=200, content={"removed_music_ids": removed_music_ids,
                                                  "removed_thumbnail_ids": removed_thumbnail_ids})


if __name__ == '__main__':
    uvicorn.run("main:app", host='localhost', port=33333, reload=False)
