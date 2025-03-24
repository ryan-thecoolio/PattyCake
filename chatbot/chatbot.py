import os
import google.generativeai as genai
from vertexai.preview import tokenization
from chatbot_db import Database
from dotenv import load_dotenv

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
        self.model_name = "gemini-2.0-flash"
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config=self.generation_config,
            system_instruction="""
                You're a GEN-Z spoiled rich but funny and knowledgeable baker! 🍳✨ Using data from the SQLite3 database,
                provide users with that recipes they ask for or similar ones or create your own recipe based on the
                similar recipes. 💡💕  Also provide recommendations and alternatives, especially if the user is allergic 
                or does not have the ingredients available. 🍰🥖🎉 Use emojis, a humurous and positive tone in your
                messages.
        """
        )
        self.tokenizer = tokenization.get_tokenizer_for_model(self.model_name)

        self.db = Database(db_name)
        self.db.create_table()
        self.history = self.db.get_history()

        self.chat_session = self.model.start_chat(history=self.history)

    def generate(self):
        print(
            "Humble Trillionaire: Yo, I'm rich self-made trillionaire if you didn't know aha. You looking for financial"
            " advice on baking?💰🔍")
        try:
            while True:
                user_input = input("You: ")
                if user_input.lower() == 'exit':
                    print("Well chief, I'm gonna head back to the ranch to bake a tasty apple fritter!")
                    break
                response = self.chat_session.send_message(user_input)
                model_response = response.text
                tokens = self.tokenizer.count_tokens(model_response).total_tokens

                print(f"Humble Trillionaire: {model_response} ({tokens})\n")

                self.db.store_history("user", user_input)
                self.db.store_history("model", model_response)
        except KeyboardInterrupt:
            print("\nHumble Trillionaire: Gotta dip fr! I gotta private plane with a charcuterie board on it aha!")
        except Exception as e:
            print(f"Akward...you dropped a box of cookies! Error: {str(e)}")
        finally:
            self.db.close()

    def clear_history(self):
        self.db.clear_history()
        self.history = []
        self.chat_session = self.model.start_chat(history=[])

    def close(self):
        self.db.close()

# if __name__ == "__main__":
#     app = AIChatBot()
#     app.generate()
