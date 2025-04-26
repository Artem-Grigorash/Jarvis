# Jarvis - Voice Assistant with Memory

## Description
Jarvis is a smart voice assistant powered by OpenAI's GPT-4. It can listen to your voice commands, respond verbally, and remember your conversations. The assistant maintains both short-term memory (recent conversation) and long-term memory (semantically relevant past interactions) to provide contextually relevant responses.

## Features
- **Voice Interaction**: Speak to Jarvis and hear its responses
- **Short-term Memory**: Remembers the current conversation context
- **Long-term Memory**: Stores and retrieves relevant past interactions using semantic search
- **Powered by GPT-4**: Utilizes OpenAI's advanced language model for intelligent responses

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key

### Steps
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/Jarvis2.git
   cd Jarvis2
   ```

2. Install the required dependencies:
   ```
   pip install openai python-dotenv pyttsx3 SpeechRecognition chromadb
   ```

3. Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage
Run the main script to start Jarvis:
```
python main.py
```

Once started, Jarvis will continuously listen for your voice commands. Speak clearly into your microphone, and Jarvis will:
1. Convert your speech to text
2. Process your request with context from both short and long-term memory
3. Respond verbally using text-to-speech

## How It Works
- **main.py**: Entry point that creates an instance of the Model class and runs the main interaction loop
- **model.py**: Contains the core functionality including speech-to-text, text-to-speech, and interaction with the OpenAI API
- **memory_db.py**: Implements the long-term memory system using ChromaDB for vector storage and semantic search

## Dependencies
- openai: For accessing GPT-4
- pyttsx3: For text-to-speech functionality
- SpeechRecognition: For converting speech to text
- python-dotenv: For loading environment variables
- chromadb: For vector storage and semantic search

