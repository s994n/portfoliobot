from dotenv import load_dotenv
import openai
from flask import Flask, request, jsonify
import os
from background_info import script
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
print('hello')

# Load .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# limiter = Limiter(app, key_func=get_remote_address, default_limits=["30 per day", "10 per hour"])

def get_forwarded_for():
    return request.headers.get('X-Forwarded-For', request.remote_addr)

limiter = Limiter(app, key_func=get_forwarded_for, default_limits=["30 per day", "10 per hour"])

@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/ask", methods=["POST"])
@limiter.limit("10 per hour")
def ask():
    prompt = request.json.get("prompt")

    # Combine user prompt with your background
    full_prompt = script + "User: " + prompt + "\nChatbot:"

    response = openai.Completion.create(
        engine="text-davinci-002", prompt=full_prompt, max_tokens=50
    )
    return jsonify({"answer": response["choices"][0]["text"]})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

