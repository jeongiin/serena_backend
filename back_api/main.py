import warnings

import uvicorn
from fastapi import FastAPI

try:
    from .apis import diaries, letters, chats, music, images, common
except ImportError:
    from apis import diaries, letters, chats, music, images, common

warnings.simplefilter(action='ignore', category=FutureWarning)

app = FastAPI(title="SKY FLY AI Melovision Internal API Service",
              redoc_url=None)
app.include_router(common.common_api)
app.include_router(diaries.diaries_api)
app.include_router(letters.letters_api)
app.include_router(chats.chats_api)
app.include_router(music.music_api)
app.include_router(images.images_api)


@app.get("/")
async def root():
    return {"message": "SKT FLY AI Melovision Internal API Service"}


if __name__ == '__main__':
    uvicorn.run("main:app", host='localhost', port=8000, reload=True)