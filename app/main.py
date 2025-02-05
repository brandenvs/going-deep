from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import fitz  # PyMuPDF
import requests
import os
from werkzeug.utils import secure_filename

import markdown

app = Flask(__name__)
CORS(app)

# Ollama API Configuration
OLLAMA_API_URL = "http://localhost:22345/api/chat"
MODEL_NAME = "deepseek-r1:1.5b"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    """Render the frontend HTML page."""
    return render_template("chat.html")


@app.route("/chat")
def chat_view():
    return render_template("chat.html")


@app.route('/cv-review')
def cv_review_view():
    return render_template('cv_review.html')


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""

    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text


def get_cv_review(cv_text):
    """Send extracted text to Ollama for review."""

    headers = {"Content-Type": "application/json"}
    prompt = f"""
        You are an experienced Careers Coach specializing in CV reviews. 
        Your role is to provide **constructive feedback** on the CV below. 

        **Guidelines:**
        - Do **not** rewrite the CV.
        - Identify **weak areas** that need improvement.
        - Be **concise, specific, and actionable** in your feedback.
        - Use **bullet points** for clarity.

        **CV for Review:**
        {cv_text}
        """

    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    response = requests.post(OLLAMA_API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        print(response)
        data = response.json()
        responses = data.get("message", {}).get("content").split('</think>')
        think_response = responses[0]
        final_response = responses[1]

        data = {
            "think_response": markdown.markdown(think_response), 
            "final_response": markdown.markdown(final_response)
        }
        return data

    else:
        return f"Error: {response.status_code}, {response.text}"


@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file upload and process the CV."""

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
        file.save(file_path)
        
        # Extract text from the PDF
        cv_text = extract_text_from_pdf(file_path)
        
        # Get review from Ollama
        data = get_cv_review(cv_text)
        
        think_response = data['think_response']
        final_response = data['final_response']
        
        return jsonify({
            "think_response": think_response,
            "final_response": final_response
        })
    
    return jsonify({"error": "File upload failed"}), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_prompt = data.get('text', '')
    response_text = ""

    try:
        api_response = requests.post(
            'http://localhost:11434/api/chat',
            json={
                'model': 'deepseek-r1:7b',
                'messages': [{'role': 'user', 'content': user_prompt}],
                'stream': False,
            },
            headers={'Content-Type': 'application/json'}
        )

        if api_response.status_code != 200:
            raise Exception(f"HTTP error! Status: {api_response.status_code}")

        api_data = api_response.json()
        if 'message' in api_data and 'content' in api_data['message']:
            response_text = api_data['message']['content']
        elif 'content' in api_data:
            response_text = api_data['content']

    except Exception as e:
        print(f"Error: {e}")
        response_text = "An error occurred while processing your request."

    return jsonify({'text': response_text})


if __name__ == "__main__":
    app.run(debug=True)
