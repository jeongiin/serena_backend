import io
import os
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
    output_audio = model.generate([prompt], progress=True)
    # scipy.io.wavfile.write(save_path, rate=sampling_rate, data=output_audio[0, 0].cpu().numpy())

    output_wav = io.BytesIO()  # 빈 BytesIO 객체 생성
    write(output_wav, sampling_rate, output_audio[0, 0].cpu().numpy())  # WAV 파일 형식으로 기록

    # BytesIO 객체에서 바이트 데이터 추출
    wav_bytes = output_wav.getvalue()
    return wav_bytes


if __name__ == "__main__":
    model = load_model(duration=10, model_size='small')

    output_music = genearate_music('A dreamy pop track with gentle piano melodies, emotional violin harmonies, and ethereal synthesizer textures, capturing the serene atmosphere as a rainbow appears over a city street.', model)
    output_music = io.BytesIO(output_music)

    file_name = f'test.wav'
    print(file_name)
    with open(os.path.join('./', file_name), 'wb') as f:
        f.write(output_music.read())
