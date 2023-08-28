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
async def generate_music(caption: str, genre: str, emotion: str, duration: int = 10):
    for limit in range(5):
        print(f'limit: {limit}')
        try:
            music_prompt = json.loads(generate_music_prompt(caption, genre, emotion))
        except Exception as e:
            print(e)
            continue
        else:
            invalid_flag = False
            if caption.lower() == music_prompt['prompt'].lower():
                print("Same Prompt")
                invalid_flag = True
                continue
            # if (music_prompt['genre'] != genre) or (music_prompt['genre'] not in music_prompt['prompt']):
            #     print("Different Genre")
            #     print(music_prompt['genre'])
            #     print(music_prompt['prompt'])
            #     invalid_flag = True
            #     continue
            # if music_prompt['speed'] not in music_prompt['prompt']:
            #     print("Different Speed")
            #     invalid_flag = True
            #     continue
            #
            # for instrument in music_prompt['instrument']:
            #     if instrument not in music_prompt['prompt']:
            #         print("Different Instrument")
            #         print(instrument)
            #         print(music_prompt['prompt'])
            #         invalid_flag = True
            #         break
            # if invalid_flag:
            #     continue
            #
            # for mood in music_prompt['mood']:
            #     if mood not in music_prompt['prompt']:
            #         print("Different Mood")
            #         print(mood)
            #         print(music_prompt['prompt'])
            #         invalid_flag = True
            #         break
            # if invalid_flag:
            #     continue

            break

    if invalid_flag:
        raise HTTPException(status_code=500, detail="Exceed Limit")

    try:
        model = load_model(duration=duration, model_size='small')
        output_music = genearate_music(music_prompt['prompt'], model)
        output_music = io.BytesIO(output_music)

        del model
        gc.collect()
        torch.cuda.empty_cache()

        response_headers = {
            "prompt": music_prompt['prompt'],
            "genre": music_prompt['genre'],
            "instrument": ', '.join(music_prompt['instrument']) if type(music_prompt['instrument']) is list else music_prompt['instrument'],
            "mood": ', '.join(music_prompt['mood']) if type(music_prompt['mood']) is list else music_prompt['mood'],
            "speed": music_prompt['speed']
        }
        print(response_headers)

        return StreamingResponse(output_music, headers=response_headers)

    except torch.cuda.OutOfMemoryError:
        return HTTPException(status_code=500, detail="Out of Memory")


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=44444, reload=True)
