# backend/create_json_from_csv.py
import pandas as pd
import json
import os

print("--- Starting JSON Generation from CSV ---")

# --- CONFIGURATION ---
CSV_FILE = "styles.csv"
IMAGE_FOLDER = "product_images"
OUTPUT_JSON_FILE = "products.json"
NUMBER_OF_PRODUCTS = 50 # How many products to include
# ---------------------

try:
    # 1. Read the CSV data file
    print(f"Reading data from '{CSV_FILE}'...")
    df = pd.read_csv(CSV_FILE, on_bad_lines='skip')
    print("CSV data loaded successfully.")
    
    # --- THIS IS THE NEW DEBUGGING LINE ---
    print("Columns found in CSV:", df.columns.tolist())
    # ------------------------------------

    # 2. Get a list of all images we actually have in our folder
    available_images = os.listdir(IMAGE_FOLDER)
    available_images_set = set(available_images) # Use a set for fast lookup
    print(f"Found {len(available_images)} images in '{IMAGE_FOLDER}'.")

    product_list = []
    
    # 3. Loop through the CSV rows
    print(f"Generating data for {NUMBER_OF_PRODUCTS} products...")
    for index, row in df.iterrows():
        # Construct the image filename
        image_filename = f"{row['id']}.jpg"

        if image_filename in available_images_set:
            product_data = {
                "id": int(row['id']),
                "name": row['productDisplayName'],
                "category": row['masterCategory'],
                "image_filename": image_filename
            }
            product_list.append(product_data)

        if len(product_list) >= NUMBER_OF_PRODUCTS:
            break

    # 4. Save the list to a JSON file
    with open(OUTPUT_JSON_FILE, 'w') as f:
        json.dump(product_list, f, indent=2)
    
    print(f"\n--- ✅ SUCCESS! ---")
    print(f"Successfully created '{OUTPUT_JSON_FILE}' with {len(product_list)} products.")

except FileNotFoundError:
    print(f"\n--- ❌ FAILED! ---")
    print(f"ERROR: The file '{CSV_FILE}' was not found.")
except KeyError as e:
    print(f"\n--- ❌ FAILED! ---")
    print(f"An error occurred: A column was not found. The missing column is: {e}")
    print("Please check the column names printed above and ensure they match the script.")
except Exception as e:
    print(f"\n--- ❌ FAILED! ---")
    print(f"An unexpected error occurred: {e}")