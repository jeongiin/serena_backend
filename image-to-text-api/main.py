import warnings

import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.responses import JSONResponse

# from emotion_classification import sort_emotion_by_score
from image_to_text import image_to_text

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

app = FastAPI(title="SKT FLY AI Melovision Internal Image to Text Service",
              redoc_url=None)


@app.get("/")
async def root():
    return {"message": "SKT FLY AI Melovision Internal Image to Text Service"}


# @app.get("/emotions", deprecated=True)
# async def get_emotions(text: str):
#     return JSONResponse(status_code=200, content=sort_emotion_by_score(text))


@app.post("/caption")
async def get_caption(image: UploadFile):
    caption = image_to_text(image.file)
    print(caption[0])
    return JSONResponse(status_code=200, content={"caption": caption[0]})


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=55555, reload=True)
