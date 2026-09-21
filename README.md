# Emotion Detection Web Application

Final project for **Developing AI Applications with Python and Flask** (IBM).

An AI-based web app that analyses customer feedback text and detects the
emotion expressed (anger, disgust, fear, joy, sadness) using the embeddable
Watson NLP library. The app is packaged as the `EmotionDetection` Python
package and deployed with Flask.

## Project structure

```
EmotionDetection/
    __init__.py              # exposes emotion_detector
    emotion_detection.py     # calls Watson NLP EmotionPredict
templates/index.html         # front end
static/mywebscript.js        # front-end script
server.py                    # Flask web server
test_emotion_detection.py    # unit tests
requirements.txt
```

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```python
from EmotionDetection import emotion_detector
emotion_detector("I am so happy I am doing this.")
```

Run the unit tests:

```bash
python3 -m unittest test_emotion_detection.py
```

Start the web server (then open http://localhost:5000):

```bash
python3 server.py
```

Static code analysis:

```bash
pylint server.py
```
