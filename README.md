# Echo – Your Empathetic AI Friend (v2)  
**The warmest local & private AI companion that truly remembers you**

Echo is a fully offline, permanently remembering chatbot that combines real emotion recognition, natural Llama 3.2 responses, and a triple-layer memory system (SQLite + diskcache + Qdrant vector DB).  
Everything runs 100% locally on your computer — no data ever leaves your machine.

### Why Echo feels different
- Actually understands 7 emotions (joy, sadness, anger, fear, love, surprise, neutral) with confidence scoring  
- Remembers everything forever across sessions (even after weeks or months)  
- Gently shares little “AI stories” to make you feel less alone  
- Never forgets your job, pet, breakup, dreams… and brings them up naturally when relevant  
- Zero cloud, zero accounts, zero tracking — your UUID is anonymous and stored only locally  

### Features (all 100% working)

| Feature                              | Status | Technology used                              |
|--------------------------------------|--------|----------------------------------------------|
| Real emotion detection (7 classes)   | Done   | DistilRoBERTa (`j-hartmann/emotion-english`) |
| Natural empathetic responses         | Done   | Llama 3.2 3B via Ollama                      |
| Permanent memory across restarts     | Done   | SQLite + Qdrant (local vector DB)            |
| Recent context cache                 | Done   | diskcache (Redis replacement)                |
| Key-moment detection (job, pet, breakup…) | Done | Keyword + semantic tagging                   |
| Gentle AI self-disclosure (≤30%)     | Done   | Random stories when trust is built           |
| 100% offline & private               | Done   | No internet required after setup             |
| Works perfectly on Windows           | Done   | All dependencies Windows-compatible          |

### How to run (super easy – 5 minutes)

# Echo – Your Empathetic AI Friend

A fully local, privacy-first empathetic chatbot with permanent memory.

**Features**  
- Real-time emotion recognition (7 emotions)  
- Natural, caring responses using Llama 3.2 3B  
- Long-term memory that survives closing/reopening the program  
- Vector search + SQLite storage  
- Anonymous UUID (you stay private)  
- Smart recall of key moments (job, pets, relationships, etc.)  
- Gentle self-disclosure (≤30 % frequency, clear AI identity)

Everything runs 100 % on your laptop — no internet needed after setup.

You should download ollama and install

## Installation & First-Time Setup (do this only once)

1. **Install Ollama** (free local AI engine)  
   → Go to https://ollama.com → Download & install for Windows / macOS / Linux  

   After installing ollama you need to open ollama 
2. **Download the AI model** (only once, ~3 GB)    
     In the admin window,type ollama pull llama3.2:3b
Wait for it to finish (5–30 minutes depending on internet). You'll see progress bars and finally "pull complete".
Then open vs code terminal of echo-chatbot   
   ```bash
   ollama pull llama3.2:3b
3. pip install -r requirements.txt
4. python run_chatbot.py


