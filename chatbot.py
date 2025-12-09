# chatbot.py
from empathy_engine import get_emotion
from memory import AdvancedMemory
import ollama
import json
import random
import os

# Load self-disclosure stories
with open('stories.json', encoding='utf-8') as f:
    STORIES = json.load(f)

class EchoChatbot:
    def __init__(self):
        self.memory = AdvancedMemory()
        self.turn_count = 0

    def respond(self, user_input):
        self.turn_count += 1
        emotion, confidence = get_emotion(user_input)

        # Retrieve memories and key moments
        past_memories = self.memory.get_relevant_memories(user_input, n=3)
        key_moments = self.memory.get_key_moments()

        memory_context = ""
        if past_memories:
            memory_context += "Things you told me before:\n" + "\n".join(past_memories) + "\n"
        if key_moments:
            memory_context += "Important things about you: " + " | ".join(key_moments[:3])

        # Occasionally share a story (≤30% chance after turn 3)
        story = ""
        if self.turn_count >= 3 and confidence > 0.7 and random.random() < 0.3:
            story = "\n\n" + random.choice(STORIES)

        # Final prompt to Llama 3.2
        prompt = f"""You are Echo, a warm and caring AI friend. You are not human, but you truly care.
Respond naturally, with empathy, in 1-3 sentences. Stay calm and kind.

User just said: "{user_input}"
Detected emotion: {emotion} (confidence: {confidence:.2f})

{memory_context}

{story}

Reply only with your message, no quotes or explanations:"""

        try:
            response = ollama.generate(model='llama3.2:3b', prompt=prompt)
            reply = response['response'].strip()
        except Exception as e:
            reply = "I'm here with you... That sounds really tough."

        # Save to memory
        self.memory.add_exchange(user_input, reply, emotion)
        return reply