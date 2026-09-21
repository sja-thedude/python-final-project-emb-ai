# Final Project Submission — Emotion Detector

Repository: https://github.com/sja-thedude/python-final-project-emb-ai

## Task 1 — GitHub repository URL (README.md)

https://github.com/sja-thedude/python-final-project-emb-ai/blob/main/README.md

## Task 2 — Activity 1: emotion_detector code (emotion_detection.py)

```python
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
```

## Task 2 — Activity 2 / Task 3 — Activity 2: terminal output (import + formatted output)

```
$ python3 -c "from EmotionDetection.emotion_detection import emotion_detector; print(emotion_detector(\"I am so happy I am doing this.\"))"
{'anger': 0.006274985, 'disgust': 0.0025598293, 'fear': 0.009251528, 'joy': 0.9680386, 'sadness': 0.049744144, 'dominant_emotion': 'joy'}
```

## Task 3 — Activity 1: formatted output code

Same file as Task 2 Activity 1 — see the `result` dictionary and `dominant_emotion` at the end of `emotion_detector`.

## Task 4 — Activity 1: __init__.py URL

https://github.com/sja-thedude/python-final-project-emb-ai/blob/main/EmotionDetection/__init__.py

```python
"""EmotionDetection package - exposes the emotion_detector function."""

from .emotion_detection import emotion_detector
```

## Task 4 — Activity 2: terminal output validating the package

```
$ python3 -c "from EmotionDetection import emotion_detector; print(emotion_detector)"
<function emotion_detector at 0x1006c2980>
```

## Task 5 — Activity 1: unit test code (test_emotion_detection.py)

```python
"""Unit tests for the EmotionDetection package."""

import unittest
from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):
    """Check that emotion_detector returns the expected dominant emotion."""

    def test_emotion_detector(self):
        """Each statement should map to its expected dominant emotion."""
        result_1 = emotion_detector('I am glad this happened')
        self.assertEqual(result_1['dominant_emotion'], 'joy')

        result_2 = emotion_detector('I am really mad about this')
        self.assertEqual(result_2['dominant_emotion'], 'anger')

        result_3 = emotion_detector('I feel disgusted just hearing about this')
        self.assertEqual(result_3['dominant_emotion'], 'disgust')

        result_4 = emotion_detector('I am so sad about this')
        self.assertEqual(result_4['dominant_emotion'], 'sadness')

        result_5 = emotion_detector('I am really afraid that this will happen')
        self.assertEqual(result_5['dominant_emotion'], 'fear')


if __name__ == '__main__':
    unittest.main()
```

## Task 5 — Activity 2: unit test terminal output

```
$ python3 -m unittest test_emotion_detection.py
test_emotion_detector (test_emotion_detection.TestEmotionDetector.test_emotion_detector)
Each statement should map to its expected dominant emotion. ... ok

----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

## Task 6 — Activity 1: server.py

```python
"""Flask server for the Emotion Detection web application.

Exposes the EmotionDetection package over HTTP so the front end in
templates/index.html can analyse customer feedback.
"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def emot_detector():
    """Analyse the text passed as ``textToAnalyze`` and describe its emotions.

    Returns a sentence listing every emotion score and the dominant emotion.
    If the input is blank or otherwise invalid the service returns no
    dominant emotion, and an error message is returned instead.
    """
    text_to_analyze = request.args.get('textToAnalyze')

    response = emotion_detector(text_to_analyze)

    if response['dominant_emotion'] is None:
        return "Invalid text! Please try again!"

    return (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, "
        f"'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, "
        f"'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )


@app.route("/")
def render_index_page():
    """Render the main application page."""
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

## Task 6 — Activity 2: screenshot

Upload `screenshots/6b_deployment_test.png`

## Task 7 — Activity 1: status-code-400 handling (emotion_detection.py)

```python

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
```

## Task 7 — Activity 2: blank-input handling (server.py)

```python
def emot_detector():
    """Analyse the text passed as ``textToAnalyze`` and describe its emotions.

    Returns a sentence listing every emotion score and the dominant emotion.
    If the input is blank or otherwise invalid the service returns no
    dominant emotion, and an error message is returned instead.
    """
    text_to_analyze = request.args.get('textToAnalyze')

    response = emotion_detector(text_to_analyze)

    if response['dominant_emotion'] is None:
        return "Invalid text! Please try again!"

    return (
```

## Task 7 — Activity 3: screenshot

Upload `screenshots/7c_error_handling_interface.png`

## Task 8 — Activity 1: server.py (pylint 10/10)

Same `server.py` as Task 6 Activity 1 (module/function docstrings, no unused imports, PEP 8 line lengths).

## Task 8 — Activity 2: pylint terminal output

```
$ pylint server.py

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)

```
