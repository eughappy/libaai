# file: libaai_blank.py
from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import pytesseract
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load a simple transformer pipeline (placeholder)
classifier = pipeline("text-classification", model="bhadresh-savani/bert-base-uncased-emotion")

# Minimal intent map (mocked)
INTENT_MAP = {
    "joy": ("event", "This seems related to events in SF."),
    "sadness": ("school", "Sounds like you're asking about schools."),
    "surprise": ("restaurant", "You're probably looking for restaurants or stores."),
    "anger": ("faq", "This could be a common question. Check the FAQs."),
    "fear": ("fallback", "Let me connect you to a human assistant.")
}

@app.route("/")
def home():
    return render_template("chat_template.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return '''
        <!doctype html>
        <html>
        <head><title>Upload Image</title></head>
        <body>
        <h2>Upload Image for OCR</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="image">
            <input type="submit" value="Upload">
        </form>
        </body>
        </html>
        '''

    file = request.files.get("image")
    if not file:
        return "No file uploaded", 400
    path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(path)
    text = pytesseract.image_to_string(Image.open(path)).strip()
    return jsonify({"extracted_text": text or "No text found."})

@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "")
    label = classifier(msg)[0]["label"].lower()
    intent, reply = INTENT_MAP.get(label, ("fallback", "I'm not sure. Connecting you to live support."))
    return jsonify({"intent": intent, "response": reply})

if __name__ == "__main__":
    app.run(debug=True)
