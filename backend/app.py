# backend/app.py
import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

app = Flask(__name__)
CORS(app)

# --- AI MODEL & DATABASE LOADING (Runs ONCE at startup) ---
print("Loading AI Model and Product Database...")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
print("AI Model loaded.")

with open('products.json', 'r') as f:
    product_database = json.load(f)

for product in product_database:
    # Ensure embedding exists before converting
    if 'embedding' in product and product['embedding']:
        product['embedding'] = torch.tensor(product['embedding'])
print(f"Product database loaded with {len(product_database)} items.")
# -------------------------------------------------------------

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('product_images', filename)

@app.route('/api/find_similar', methods=['POST'])
def find_similar():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # 1. Process the User's Uploaded Image
        uploaded_image = Image.open(file.stream)
        inputs = processor(images=uploaded_image, return_tensors="pt", padding=True)
        with torch.no_grad():
            uploaded_image_features = model.get_image_features(**inputs)

        # 2. Calculate Similarity Scores
        similarities = []
        for product in product_database:
            # Skip any product that might be missing an embedding
            if 'embedding' not in product or not isinstance(product['embedding'], torch.Tensor):
                continue

            similarity_score = torch.nn.functional.cosine_similarity(
                uploaded_image_features,
                product['embedding'].unsqueeze(0)
            ).item()
            
            similarities.append({
                "product": product,
                "score": similarity_score
            })
        
        # 3. Sort Products by Score
        sorted_products = sorted(similarities, key=lambda x: x['score'], reverse=True)

        # 4. Return the Top 5 Matches (CORRECTED, SAFE VERSION)
        # Create a clean list of results to avoid modifying the in-memory database.
        top_5_results = []
        for match in sorted_products[:5]:
            # Create a new dictionary with only the info the frontend needs.
            product_details = {
                "id": match['product']['id'],
                "name": match['product']['name'],
                "category": match['product']['category'],
                "image_filename": match['product']['image_filename']
            }
            
            top_5_results.append({
                "product_details": product_details,
                "similarity_score": match['score']
            })

        return jsonify(top_5_results)

    except Exception as e:
        print(f"Error processing image: {e}")
        return jsonify({'error': f'An error occurred: {e}'}), 500

# At the very bottom of backend/app.py

if __name__ == '__main__':
    # Get the port from the environment variable, defaulting to 5000 for local development
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)