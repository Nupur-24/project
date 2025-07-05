from flask import Flask, request, jsonify
from PIL import Image
import hashlib
import io
import os

app = Flask(__name__)

# Store previously seen hashes to simulate duplication check
seen_hashes = set()

@app.route('/')
def home():
    return "✅ Flask Image Fraud Detection API is live!"

@app.route('/check_image', methods=['POST'])
def check_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    image_bytes = file.read()

    # Generate hash for duplication check
    image_hash = hashlib.md5(image_bytes).hexdigest()

    # Check for duplication
    is_duplicate = image_hash in seen_hashes
    seen_hashes.add(image_hash)

    # Check format and dimensions
    try:
        image = Image.open(io.BytesIO(image_bytes))
        width, height = image.size
        format = image.format
    except Exception as e:
        return jsonify({"error": f"Invalid image: {str(e)}"}), 400

    return jsonify({
        "filename": file.filename,
        "hash": image_hash,
        "width": width,
        "height": height,
        "format": format,
        "is_duplicate": is_duplicate
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
