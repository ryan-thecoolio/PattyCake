# app.py
from flask import Flask, render_template, request, jsonify
from chatbot.chatbot import AIChatBot
from chatbot.chatbot_db import Database


app = Flask(__name__)

chatbot = AIChatBot()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']  # Get the user's message from the form

    # Get the bot response using the AIChatBot class
    bot_response = chatbot.chat_session.send_message(user_message).text

    # Optionally, store the conversation history in the database
    chatbot.db.store_history("user", user_message)
    chatbot.db.store_history("model", bot_response)

    # Return the bot response as JSON to update the UI
    return jsonify({'message': bot_response})


@app.route('/clear_history', methods=['POST'])
def clear_history():
    chatbot.clear_history()  # Clear chat history
    return jsonify({'message': 'Chat history cleared'})


if __name__ == '__main__':
    app.run(debug=True)
