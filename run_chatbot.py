# run_chatbot.py
from chatbot import EchoChatbot
import time
import os

def slow_print(text):
    for char in text + "\n":
        print(char, end='', flush=True)
        time.sleep(0.018)

# Create folders if missing
os.makedirs("users", exist_ok=True)
os.makedirs("chroma_db", exist_ok=True)

print("="*70)
print("                  ECHO – Your Empathetic Friend (v2)")
print("           Now with permanent memory across sessions!")
print("="*70)

slow_print("Hi! I'm Echo. I will remember everything you tell me,")
slow_print("even if you close and reopen this program.")
slow_print("Type 'bye' when you want to go.\n")

bot = EchoChatbot()

while True:
    try:
        user = input("You: ").strip()
    except:
        break

    if not user:
        continue
    if user.lower() in ["bye", "quit", "exit", "goodbye", "tata"]:
        slow_print("\nTake care of yourself. I'll always be here when you come back ♡")
        break

    reply = bot.respond(user)
    slow_print(f"Echo: {reply}\n")