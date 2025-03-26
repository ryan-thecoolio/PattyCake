from flask import Flask, render_template, request, jsonify, g
from chatbot.chatbot import AIChatBot
from chatbot.chatbot_db import Database

app = Flask(__name__)
chatbot = AIChatBot()


def format_recipe(recipe_text):
    """Formats a recipe string based on Markdown-like syntax."""

    lines = recipe_text.split('\n')
    formatted_lines = []

    for line in lines:
        line = line.strip()  # Remove leading/trailing spaces

        if line.startswith('##'):
            formatted_lines.append(f"<b>{line[2:].strip()}</b>")  # Heading
        else:
            # Handle bold text
            while '**' in line:
                start = line.find('**')
                end = line.find('**', start + 2)
                if end == -1:
                    break  # Handle unmatched **
                bold_text = line[start + 2:end]
                line = line.replace(f"**{bold_text}**", f"<b>{bold_text}</b>")
            formatted_lines.append(line)  # Plain text or bold text

    return '<br>'.join(formatted_lines)  # Join lines with HTML line breaks


def get_db():
    if 'db' not in g:
        g.db = Database()
    return g.db


@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/process", methods=["POST"])
def process():
    db = get_db()
    try:
        user_message = request.get_json()['value']

        recipe_text = chatbot.model.generate_content(user_message).text
        result = format_recipe(recipe_text)

        db.store_history('user', user_message)
        db.store_history('model', recipe_text)

        return jsonify(result=result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
