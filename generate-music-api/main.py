import gc
import io
import json
import warnings

import torch
import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.responses import StreamingResponse

from chatgpt import generate_music_prompt
from music_generator import genearate_music, load_model

warnings.simplefilter(action='ignore', category=FutureWarning)

app = FastAPI(title="SKT FLY AI Melovision Internal Music GEN Service",
              redoc_url=None)


@app.get("/")
async def root():
    return {"message": "SKT FLY AI Melovision Internal Music GEN Service"}


@app.get("/music")
async def generate_music(caption: str, genre: str):
    while True:
        try:
            music_prompt = json.loads(generate_music_prompt(caption, genre))
        except:
            continue
        else:
            break

    try:
        model = load_model(duration=10)
        output_music = genearate_music(music_prompt['prompt'], model)
        output_music = io.BytesIO(output_music)

        del model
        gc.collect()
        torch.cuda.empty_cache()

        response_headers = {
            "prompt": music_prompt['prompt'],
            "genre": music_prompt['genre'],
            "instrument": ', '.join(music_prompt['instrument']),
            "mood": ', '.join(music_prompt['mood']),
            "speed": music_prompt['speed']
        }

        return StreamingResponse(output_music, headers=response_headers)

    except torch.cuda.OutOfMemoryError:
        return HTTPException(status_code=500, detail="Out of Memory")


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=44444, reload=True)
