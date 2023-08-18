#!pip install transformers -q
#!pip install googletrans==3.1.0a0
from transformers import pipeline
import googletrans
import time


#텍스트 영어로 번역
def translate_text(text):
    translator = googletrans.Translator()
    en_taedam = translator.translate(taedam, dest='en', src='ko')
    return(en_taedam.text)

#top1 감정 키워드 반환
def emotion_classifier(text):
    model = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa')
    emotion = model(translate_text(text))[0]['label']
    return(emotion)

#score 오름차순 정렬한 감정 label과 각 score 반환
def sort_emotion_by_score(text):
    model = pipeline('sentiment-analysis', model='arpanghoshal/EmoRoBERTa', return_all_scores= True)
    sorted_data = sorted(model(translate_text(text))[0], key=lambda x: x['score'], reverse=True)
    return sorted_data

if __name__ == "__main__":
    text = "나는 널 사랑해."
  
    start = time.time()
  
    #top1 감정 키워드
    print(emotion_classifier(text))
  
    #전체 감정 키워드 정렬
    print(sort_emotion_by_score(text))
  
    print('spending time :', time.time() - start)

