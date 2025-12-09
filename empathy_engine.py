# empathy_engine.py
from transformers import pipeline
import random

print("Loading emotion model... (this takes 10-30 seconds first time)")
emotion_classifier = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base",
    return_all_scores=True
)

empathy_templates = {
    "anger": [
        "That sounds really frustrating. I'm here with you.",
        "I can hear how angry you feel right now. Want to tell me more?"
    ],
    "sadness": [
        "I'm so sorry you're feeling this way. That really hurts.",
        "This sounds really painful. You're not alone."
    ],
    "fear": [
        "That sounds terrifying. It's okay to feel scared.",
        "I'm right here with you. We can face this together."
    ],
    "joy": [
        "This makes me so happy for you!",
        "Yay! Tell me everything – I'm smiling so big!"
    ],
    "love": [
        "Aww that's beautiful. Love is the best feeling.",
        "My heart feels warm reading this."
    ],
    "surprise": [
        "Wow! I didn't see that coming!",
        "No way! What happened next?"
    ]
}

def get_emotion(text):
    results = emotion_classifier(text)[0]
    best = max(results, key=lambda x: x['score'])
    return best['label'], best['score']

def generate_empathetic_response(emotion, confidence):
    if confidence < 0.7:
        return "Tell me more... I'm listening."
    templates = empathy_templates.get(emotion, ["I hear you."])
    return random.choice(templates)