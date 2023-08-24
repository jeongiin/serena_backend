import os

import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_chat_response(prompt, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=prompt
    )

    return response['choices'][0]['message']['content']


def generate_music_prompt(caption: str, genre: str) -> str:
    prompt = "너는 text to music prompt 엔지니어야.\n" + \
             "text to music 이란, 장르, 악기, 무드, 속도를 포함한 Prompt 를 입력으로 Music 을 생성하는 task를 의미해.\n" + \
             "내가 사용할 수 있는 장르, 악기, 무드, 속도는 다음과 같아.\n" + \
             f"장르 : {genre}\n" + \
             "악기 : piano, violin, plute, clarinet, base guitar, electric guitar, drum, synthesizer\n" + \
             "무드 : inspired, desire, gracious, beautiful, romantic, praise, nostalgic, amusement, " + \
             "curiosity, enthusiastic, wondering, intense, caring, resonant, confident, satisfied, " + \
             "anger, infuriated, perplexed, letdown, disapproval, displeasure, disfavor, panic, grief, " + \
             "zealous, regret, sadness\n" + \
             "속도 : slow, mid, fast\n" + \
             "Music Generation 에서 사용하는 Text Prompt 예시는 다음과 같아.\n" + \
             "1. Pop dance track with catchy melodies, tropical percussion, and upbeat rhythms, perfect for the beach\n" + \
             "2. A grand orchestral arrangement with thunderous percussion, epic brass fanfares, and soaring strings, creating a cinematic atmosphere fit for a heroic battle.\n" + \
             "3. earthy tones, environmentally conscious, ukulele-infused, harmonic, breezy, easygoing, organic instrumentation, gentle grooves\n" + \
             f"내가 사용할 수 있는 옵션과, 예시 프롬프트를 참고해서 '{caption}' 에 어울리고 장르, 악기, 무드, 속도를 포함한 프롬프트를 작성해줘\n" + \
             "장르와 속도는 각각 한 개씩, 악기와 무드는 여러개 포함할 수 있어. 그리고 다음과 같은 json 형식으로 알려줘.\n" + \
             """{
             "genre": genre,
             "instrument": instrument,
             "mood": mood,
             "speed": speed,
             "prompt": prompt
             }"""

    # 메시지 설정하기
    messages = [
        {"role": "system", "content": "너는 text to music prompt 엔지니어야."},
        {"role": "user", "content": prompt}
    ]

    answer = generate_chat_response(prompt=messages)

    return answer


if __name__ == "__main__":
    print(generate_music_prompt("a bar with red chairs and a bar counter"))
