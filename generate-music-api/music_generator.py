import io
import time
import warnings

from audiocraft.models import musicgen
from scipy.io.wavfile import write

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)


def generate_prompt(options: dict):
    prompt = 'a ' + options['genre'] + ' track with ' + ' and '.join(options['instrument']) + ' at ' + options['speed'] + ' bpm' + ' calm'
    print(prompt)
    return prompt


def load_model(model_size='small', duration=30):
    model = musicgen.MusicGen.get_pretrained(model_size, device='cuda')
    model.set_generation_params(duration=duration)
    return model


def genearate_music(prompt, model, sampling_rate=32000):
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
    options = {'genre': '80s driving pop', 'instrument': ['heavy drums'],
               'speed': 'slow', 'mood': 'calm'}
    prompt = generate_prompt(options)
    file_name = prompt.replace(' ', '_') + '.wav'
    print(file_name)
    start = time.time()
    genearate_music(prompt, model, save_path=file_name)
    print('spending time :', time.time() - start)
