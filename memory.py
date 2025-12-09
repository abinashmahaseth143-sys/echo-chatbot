# memory.py
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

class Memory:
    def __init__(self):
        self.history = []
        self.embeddings = []

    def add_exchange(self, user_text, bot_text, emotion):
        self.history.append({"user": user_text, "bot": bot_text, "emotion": emotion})
        embedding = model.encode(user_text)
        self.embeddings.append(embedding)

        if len(self.history) > 10:
            self.history.pop(0)
            self.embeddings.pop(0)

        # Simple key moment detection
        lower = user_text.lower()
        if any(word in lower for word in ["job", "work", "fired", "quit", "boss"]):
            print("(Memory note: User talked about work/job)")
        if any(word in lower for word in ["pet", "dog", "cat", "puppy", "kitten"]):
            print("(Memory note: User mentioned a pet)")

    def get_relevant_memory(self, current_text):
        if len(self.embeddings) == 0:
            return None
        import numpy as np
        current_emb = model.encode(current_text)
        similarities = [np.dot(current_emb, emb) for emb in self.embeddings]
        best_idx = similarities.index(max(similarities))
        if similarities[best_idx] > 0.6:
            return self.history[best_idx]["user"]
        return None