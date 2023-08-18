import asyncio
import warnings

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse, JSONResponse

from emotion_classification import sort_emotion_by_score

warnings.simplefilter(action='ignore', category=FutureWarning)

app = FastAPI(title="SKT FLY AI Melovision Internal Emotions Classify Service",
              redoc_url=None)


@app.get("/")
async def root():
    return {"message": "SKT FLY AI Melovision Internal Emotions Classify Service"}


@app.get("/emotions")
async def get_emotions(text: str):
    return JSONResponse(status_code=200, content=sort_emotion_by_score(text))


@app.get("/stream")
async def stream():
    async def event_generator():
        for i in range(10):
            yield f"data: Event {i}\n\n"
            await asyncio.sleep(1)  # 1초마다 새 이벤트 전송

    return StreamingResponse(event_generator(), media_type="text/event-stream")


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=56789, reload=True)
