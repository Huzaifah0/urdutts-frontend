# Urdu LLM Voice Assistant - CM Punjab Easy Karobar Finance

This project is an **Urdu-speaking AI voice assistant** built to answer questions about the **CM Punjab Easy Karobar Finance Scheme**. It uses a custom **Large Language Model (LLM)** backed by Qalb-1.0-8B-Instruct and supports **voice-to-voice interactions** via speech recognition (STT) and text-to-speech (TTS).

---

## Features

- **Urdu LLM**: Provides accurate answers based on the Punjab finance KB (`urdu_kb.txt`).  
- **Voice-to-Voice Interface**: Converts user speech to text, generates an answer, and converts it back to speech.  
- **Chunked Knowledge Base**: Handles long KB content efficiently for precise LLM responses.  
- **Strict Single-Answer Enforcement**: The assistant avoids repeating answers or adding unnecessary explanations.  
- **Logging**: Tracks LLM input/output and any preprocessing steps for debugging.

---

## Installation

1. Clone the repository:

```bash
git clone <repository_url>
cd <repository_folder>


Create a Python virtual environment:

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows


Install dependencies:

pip install -r requirements.txt


Make sure urdu_kb.txt is in the same folder as llm/model.py.

Usage
Import and generate response
from llm.model import generate

user_question = "سی ایم پنجاب کاروبار سکیم میں کون اہل ہے؟"
response = generate(user_question)
print(response)

Voice-to-Voice API

Use the /voice_to_voice endpoint (if running a FastAPI or Flask backend) to convert spoken Urdu input into audio response.

File Structure
project/
│
├─ llm/
│  ├─ model.py           # LLM loading, KB handling, response generation
│  └─ urdu_kb.txt        # Knowledge base text file
│
├─ main.py               # Example script / API entrypoint
├─ requirements.txt      # Python dependencies
├─ README.md
└─ .gitignore

Notes / Recommendations

TTS Limitations: Urdu TTS currently supports ~250 characters per request. For long answers, consider splitting output into chunks before sending to TTS.

KB Updates: You can update urdu_kb.txt freely; the LLM reads it dynamically and caches it in memory.

Chunking & Searching: The KB is internally chunked for better LLM recall and relevance matching.

Logging

The system logs:

LLM input and output lengths

User queries

Cleaning of repeated phrases or extra labels in the LLM output

KB loading and caching

All logs are handled via Python's standard logging module.