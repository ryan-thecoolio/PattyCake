import os
import google.generativeai as genai
from .chatbot_db import Database


class AIChatBot:
    def __init__(self, db_name="chat_history.db"):

        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        # Create the model
        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 1024,
            "response_mime_type": "text/plain",
        }
        self.model_name = "tunedModels/baker-v4-brvq2fh93ca5"
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config,
        )

        self.db = Database(db_name)
        self.db.create_table()
        self.history = self.db.get_history()

        self.chat_session = self.model.start_chat(history=self.history)

    def generate(self, user_message):
        try:
            if user_message.lower() == 'exit':
                print("Baking Assistant: Catch ya later!  Gotta go chase some food trucks! 🚚💨")
            response = self.chat_session.send_message(user_message)
            model_response = response.text
            print(model_response)
            self.db.store_history("user", user_message)
            self.db.store_history("model", model_response)
        except Exception as e:
            return f"Whoa, Gordon Ramsay is having a kitchen meltdown! 🤯  Error: {str(e)}  (Don't worry, we'll fix it!)"

    def clear_history(self):
        self.db.clear_history()
        self.history = []
        self.chat_session = self.model.start_chat(history=[])

    def close(self):
        self.db.close()
