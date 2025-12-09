# run_chatbot.py
from chatbot import EchoChatbot
import time

def slow_print(text):
    for char in text + "\n":
        print(char, end='', flush=True)
        time.sleep(0.02)

print("="*60)
print("                   ECHO – Your Empathetic Friend")
print("="*60)
slow_print("Hello! I'm Echo. You can tell me anything – I'm here to listen.")
slow_print("Type 'bye' when you want to stop.\n")

bot = EchoChatbot()

while True:
    try:
        user = input("You: ")
    except:
        break
        
    if user.strip() == "":
        continue
    if user.lower() in ["bye", "quit", "exit", "goodbye"]:
        slow_print("\nTake care of yourself. I'll always be here if you need me.")
        break

    reply = bot.respond(user)
    slow_print(f"Echo: {reply}")