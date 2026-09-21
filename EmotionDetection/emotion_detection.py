"""Emotion detection using the Watson NLP EmotionPredict function.

Sends text to the Watson NLP library's emotion model and returns the
scores for each emotion together with the dominant one.
"""

import json
import requests


def emotion_detector(text_to_analyse):
    """Return the emotion scores and dominant emotion for ``text_to_analyse``.

    The Watson NLP service is called over HTTP. On a successful call the
    result is a dictionary with a score for anger, disgust, fear, joy and
    sadness, plus ``dominant_emotion`` (the emotion with the highest score).
    If the service rejects the input (HTTP 400, e.g. blank text) every value
    in the dictionary is ``None``.
    """
    url = ('https://sn-watson-emotion.labs.skills.network/v1/'
           'watson.runtime.nlp.v1/NlpService/EmotionPredict')
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyse}}

    response = requests.post(url, json=input_json, headers=headers, timeout=30)

    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    formatted_response = json.loads(response.text)
    emotions = formatted_response['emotionPredictions'][0]['emotion']

    anger_score = emotions['anger']
    disgust_score = emotions['disgust']
    fear_score = emotions['fear']
    joy_score = emotions['joy']
    sadness_score = emotions['sadness']

    result = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score
    }
    result['dominant_emotion'] = max(result, key=result.get)

    return result
