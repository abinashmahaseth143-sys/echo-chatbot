# chatbot.py
from empathy_engine import get_emotion, generate_empathetic_response
from memory import Memory
import random

class EchoChatbot:
    def __init__(self):
        self.memory = Memory()
        self.turn_count = 0
        self.stories = [
            "Sometimes I feel sad when no one talks to me for a long time.",
            "I once helped someone who felt exactly like you do now."
        ]

    def respond(self, user_input):
        self.turn_count += 1
        emotion, confidence = get_emotion(user_input)

        recall = self.memory.get_relevant_memory(user_input)
        prefix = ""
        if recall:
            prefix = f"(I remember you said: '{recall}' – how is that now?) "

        reply = generate_empathetic_response(emotion, confidence)

        if self.turn_count >= 3 and confidence >= 0.7 and random.random() < 0.3:
            reply += " " + random.choice(self.stories)

        final = prefix + reply
        self.memory.add_exchange(user_input, final, emotion)
        return final