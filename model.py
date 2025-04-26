import os

import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
from openai import OpenAI

from memory_db import MemoryDB


class Model:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        self.message_history = [{"role": "system", "content": "You are a smart voice assistant."}]
        self.memory_db = MemoryDB()

    def ask_model(self, question):
        self.memory_db.save('user', question)
        memories = self.memory_db.smart_search(query=question, limit=3)
        if memories:
            print("Information from long-term memory:")
            for m in memories:
                print(f"    • {m['role']}: {m['content']}")
            mem_str = "\n".join([f"{m['role']}: {m['content']}" for m in memories])
        else:
            mem_str = ""

        print("Information from short-term memory:")
        for m in self.message_history:
            print(f"    • {m['role']}: {m['content']}")
        short_str = "\n".join([f"{m['role']}: {m['content']}" for m in self.message_history])

        prompt_messages = [
            {"role": "system", "content": f"Short-term memory (conversation history):\n{short_str}"}
        ]
        if mem_str:
            prompt_messages.append({
                'role': 'system',
                'content': f"Long-term memory (relevant past):\n{mem_str}"
            })
        prompt_messages.append({'role': 'user', 'content': question})

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=prompt_messages
        )

        model_reply = response.choices[0].message.content
        self.memory_db.save('assistant', model_reply)

        self.message_history.append({'role': 'user', 'content': question})
        self.message_history.append({'role': 'assistant', 'content': model_reply})
        if len(self.message_history) > 30:
            self.message_history = self.message_history[-30:]

        return model_reply

    def text_to_speech(self, text):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)

        recognizer.pause_threshold = 2.0
        recognizer.non_speaking_duration = 1.0
        recognizer.dynamic_energy_threshold = False

        try:
            with sr.Microphone() as source:
                print("🗣️ Please speak now; listening...")
                audio_data = recognizer.listen(
                    source,
                    timeout=None,
                    phrase_time_limit=None
                )
                print("🔊 Audio successfully recorded")
        except sr.WaitTimeoutError:
            print("❌ Wait timeout: no speech detected.")
            return None

        try:
            text = recognizer.recognize_google(audio_data, language="en-US")
            print(f"✅ You said: {text}")
            return text
        except sr.UnknownValueError:
            print("❌ Error: unable to understand the input.")
            return None
        except sr.RequestError as e:
            print(f"❌ Network or API error occurred: {e}")
            return None

    def ask_model_with_speech(self):
        audio_text = self.speech_to_text()
        if audio_text:
            model_response = self.ask_model(audio_text)
            print(f"💬 Model response: {model_response}")
            self.text_to_speech(model_response)
            return model_response
        else:
            print("❌ No valid speech input detected.")
            return None
