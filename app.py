from flask import Flask, request, jsonify, render_template
import requests
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
import os

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True  # Force reload templates

@app.after_request
def add_header(response):
    """Ensure templates & static files are not cached"""
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

credentials = Credentials(
    url="https://us-south.ml.cloud.ibm.com",
    api_key="your-api-key"
)

client = APIClient(credentials)

model = ModelInference(
    model_id="meta-llama/llama-3-405b-instruct",
    api_client=client,
    space_id="your-space-id",
    params={
        "max_new_tokens": 100
    }
)

chat_history = []

@app.route("/")
def index():
    return render_template("index.html", chat_history=chat_history)

@app.route("/send", methods=["POST"])
def send():
    global chat_history
    user_input = request.form.get("user_input")
    
    if user_input:
        chat_history.append(("User", user_input))
        full_prompt = "\n".join([f"{role}: {message}" for role, message in chat_history])
        response = model.generate_text(full_prompt)
        chat_history.append(("Model", response))
    
    return jsonify({"chat_history": chat_history})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
