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

# Load the AI model from the cache (this will be fast)
MODEL_NAME = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(MODEL_NAME)
processor = CLIPProcessor.from_pretrained(MODEL_NAME)
print("AI Model loaded.")

# Load the product database with embeddings into memory
with open('products.json', 'r') as f:
    product_database = json.load(f)

# Convert all product embeddings from lists to PyTorch Tensors for fast computation
for product in product_database:
    product['embedding'] = torch.tensor(product['embedding'])
print(f"Product database loaded with {len(product_database)} items.")
# -------------------------------------------------------------

# --- API Route to serve product images ---
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('product_images', filename)
# -----------------------------------------

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
        # We'll use Cosine Similarity, a standard for comparing vectors
        similarities = []
        for product in product_database:
            # Calculate cosine similarity between the uploaded image and a product in the database
            similarity_score = torch.nn.functional.cosine_similarity(
                uploaded_image_features,
                product['embedding'].unsqueeze(0) # Add a dimension to match
            ).item() # .item() gets the single number from the tensor
            
            similarities.append({
                "product": product,
                "score": similarity_score
            })
        
        # 3. Sort Products by Score
        # We sort in descending order to get the highest scores first
        sorted_products = sorted(similarities, key=lambda x: x['score'], reverse=True)

# backend/app.py

        # 4. Return the Top 5 Matches (NEW, SAFER VERSION)
        # Create a clean list of results to send to the frontend.
        top_5_results = []
        for match in sorted_products[:5]:
            # Create a new dictionary with only the information the frontend needs.
            # This avoids modifying the original database objects.
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)