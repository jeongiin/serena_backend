import warnings

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

try:
    from .apis import diaries, letters, chats, models, common
except ImportError:
    from apis import diaries, letters, chats, models, common

warnings.simplefilter(action='ignore', category=FutureWarning)

app = FastAPI(title="SKT FLY AI Melovision Internal API Service",
              redoc_url=None)
app.include_router(common.common_api)
# app.include_router(diaries.diaries_api)
# app.include_router(letters.letters_api)
# app.include_router(chats.chats_api)
app.include_router(models.models_api)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    print(exc.errors())
    print(exc.body)
    return PlainTextResponse(status_code=422, content=f"detail: {exc.errors()}\nbody: {exc.body}")


@app.get("/")
async def root():
    return {"message": "SKT FLY AI Melovision Internal API Service"}


if __name__ == '__main__':
    uvicorn.run("main:app", host='localhost', port=34567, reload=False)
