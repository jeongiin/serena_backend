import io
import os
import time
import warnings

from audiocraft.models import musicgen
from scipy.io.wavfile import write

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

def load_model(model_size='small', duration=30):
    model = musicgen.MusicGen.get_pretrained(model_size, device='cuda')
    model.set_generation_params(duration=duration)
    return model


def genearate_music(prompt, model, sampling_rate=32000):
    print(prompt)
    output_audio = model.generate([prompt], progress=True)
    # scipy.io.wavfile.write(save_path, rate=sampling_rate, data=output_audio[0, 0].cpu().numpy())

    output_wav = io.BytesIO()  # 빈 BytesIO 객체 생성
    write(output_wav, sampling_rate, output_audio[0, 0].cpu().numpy())  # WAV 파일 형식으로 기록

    # BytesIO 객체에서 바이트 데이터 추출
    wav_bytes = output_wav.getvalue()
    return wav_bytes


if __name__ == "__main__":
    model = load_model()
    # An 80s driving pop song with heavy drums and synth pads in the background
    emotions = ['admiration', 'desire', 'gratitude', 'joy', 'love', 'pride', 'realization', 'amusement', 'curiocity',
                'excitement', 'surprise', 'approval', 'caring', 'neutral', 'optimism', 'relief', 'anger', 'annoyance',
                'confusion', 'disappointment', 'disapproval', 'disgust', 'embarrassment', 'fear', 'nervousness',
                'grief', 'remorse', 'sadness']
    options = {'genre': 'classic', 'instrument': ['piano', 'violin', 'plute', 'clarinet'],
               'speed': 'medium'}

    for emotion in emotions:
        path = os.path.join(os.path.dirname(__file__), 'tests', emotion)
        if not os.path.exists(path):
            os.makedirs(path)

        for i in range(3):
            options['emotion'] = emotion
            prompt = generate_prompt(options)
            file_name = prompt.replace(' ', '_') + f'_{i}.wav'
            print(file_name)
            start = time.time()
            wav_bytes = genearate_music(prompt, model)

            # 생성한 음악을 tests 폴더 안의 각 emotion 폴더에 저장
            data_stream = io.BytesIO(wav_bytes)
            with open(os.path.join(path, file_name), 'wb') as f:
                f.write(data_stream.read())

            print('spending time :', time.time() - start)
