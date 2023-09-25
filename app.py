from dotenv import load_dotenv
import openai
from flask import Flask, request, jsonify
import os
from background_info import script

# Load .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/ask", methods=["POST"])
def ask():
    prompt = request.json.get("prompt")

    # Combine user prompt with your background
    full_prompt = script + "User: " + prompt + "\nChatbot:"

    response = openai.Completion.create(
        engine="text-davinci-002", prompt=full_prompt, max_tokens=50
    )
    return jsonify({"answer": response["choices"][0]["text"]})


if __name__ == "__main__":
    app.run(debug=True)
