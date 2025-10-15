# backend/generate_embeddings.py
import json
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch # Make sure torch is imported

print("--- Starting Embedding Generation ---")

# --- CONFIGURATION ---
PRODUCTS_JSON_IN = "products.json"
PRODUCTS_JSON_OUT = "products_with_embeddings.json" # We'll save to a new file
IMAGE_FOLDER = "product_images"
MODEL_NAME = "openai/clip-vit-base-patch32"
# ---------------------

try:
    # 1. Load the AI Model (will be fast from cache)
    print(f"Loading model '{MODEL_NAME}'...")
    model = CLIPModel.from_pretrained(MODEL_NAME)
    processor = CLIPProcessor.from_pretrained(MODEL_NAME)
    print("Model loaded successfully.")

    # 2. Load the product data
    with open(PRODUCTS_JSON_IN, 'r') as f:
        products = json.load(f)
    print(f"Loaded {len(products)} products from '{PRODUCTS_JSON_IN}'.")

    # 3. Process each image and add its embedding
    for i, product in enumerate(products):
        image_path = f"{IMAGE_FOLDER}/{product['image_filename']}"
        print(f"Processing ({i+1}/{len(products)}): {image_path}")

        try:
            image = Image.open(image_path)
            inputs = processor(images=image, return_tensors="pt", padding=True)
            
            # This is a critical line for performance
            with torch.no_grad(): # Tells the model not to calculate gradients
                image_features = model.get_image_features(**inputs)

            # Convert the tensor to a simple Python list and add it to the product data
            product["embedding"] = image_features[0].tolist()

        except FileNotFoundError:
            print(f"  - WARNING: Image not found for product ID {product['id']}. Skipping.")
            product["embedding"] = None # Mark as null if image is missing

    # 4. Save the updated data to a new file
    with open(PRODUCTS_JSON_OUT, 'w') as f:
        json.dump(products, f, indent=2)

    print(f"\n--- ✅ SUCCESS! ---")
    print(f"Embeddings generated and saved to '{PRODUCTS_JSON_OUT}'.")
    print("You should now rename this file to 'products.json' to use it in your app.")

except Exception as e:
    print(f"\n--- ❌ FAILED! ---")
    print(f"An error occurred: {e}")