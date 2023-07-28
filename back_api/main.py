import warnings

import uvicorn
from fastapi import FastAPI

try:
    from .apis import diaries, letters, chats
except ImportError:
    from apis import diaries, letters, chats

warnings.simplefilter(action='ignore', category=FutureWarning)

app = FastAPI(title="SKY FLY AI Melovision Internal API Service")
app.include_router(diaries.diaries_api)
app.include_router(letters.letters_api)
app.include_router(chats.chats_api)


@app.get("/")
async def root():
    return {"message": "SKY FLY AI Melovision Internal API Service"}


if __name__ == '__main__':
    uvicorn.run("main:app", host='localhost', port=8000, reload=True)