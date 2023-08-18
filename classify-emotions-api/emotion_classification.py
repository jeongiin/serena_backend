import time
import warnings

import googletrans
from transformers import pipeline, RobertaTokenizerFast, TFRobertaForSequenceClassification

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)

tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")


# 텍스트 영어로 번역
def translate_text(text):
    translator = googletrans.Translator()
    en_taedam = translator.translate(text, dest='en', src='ko')
    return en_taedam.text


# top1 감정 키워드 반환
def emotion_classifier(text):
    emotion = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)
    emotion_data = emotion(translate_text(text))[0]['label']
    return emotion


# score 오름차순 정렬한 감정 label과 각 score 반환
def sort_emotion_by_score(text):
    emotion = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa', return_all_scores=True)
    sorted_data = sorted(emotion(translate_text(text))[0], key=lambda x: x['score'], reverse=True)
    return sorted_data


if __name__ == "__main__":
    text = "나는 널 사랑해."

    print(translate_text(text))
    start = time.time()

    # top1 감정 키워드
    print(emotion_classifier(text))

    # 전체 감정 키워드 정렬
    print(sort_emotion_by_score(text))

    print('spending time :', time.time() - start)
