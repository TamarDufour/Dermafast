
import os
import sys
from dotenv import load_dotenv

# Add project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.app.ml_model import load_model, inference
from backend.app.supabase_client import supabase_client as supabase

def populate_embeddings():
    """
    Populates the 'embedding' column in the 'ham_metadata' table for images
    in the 'HAM10000_for_comparison' bucket.
    """
    print("Starting script to populate embeddings...")

    # Load the model
    # The path is relative to the project root
    model_path = 'backend/app/ml_model/model_weights.pkl'
    print(f"Loading model from {model_path}...")
    try:
        model = load_model(model_path=model_path)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Define bucket name
    bucket_name = 'HAM10000_for_comparison'
    print(f"Accessing bucket: {bucket_name}")

    try:
        # List files in the bucket
        files = supabase.storage.from_(bucket_name).list()
        print(f"Found {len(files)} files in the bucket.")

        for i, file in enumerate(files):
            image_name = file['name']
            
            # Skip non-image files
            if not image_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                print(f"Skipping non-image file: {image_name}")
                continue

            image_id = os.path.splitext(image_name)[0]
            
            print(f"Processing file {i + 1}/{len(files)}: {image_name} (image_id: {image_id})")

            # Download image
            try:
                image_bytes = supabase.storage.from_(bucket_name).download(image_name)
                if image_bytes is None:
                    print(f"  -> Failed to download {image_name}.")
                    continue
                print(f"  -> Downloaded {image_name}.")
            except Exception as e:
                print(f"  -> An error occurred during download for {image_name}: {e}")
                continue

            # Get embedding
            try:
                _, embedding = inference(model, image_bytes)
                print(f"  -> Generated embedding with {len(embedding)} dimensions.")
            except Exception as e:
                print(f"  -> Error during inference for {image_name}: {e}")
                continue

            # Update database
            try:
                update_response = supabase.table('ham_metadata').update({'embedding': embedding}).eq('image_id', image_id).execute()
                
                if hasattr(update_response, 'error') and update_response.error:
                     print(f"  -> Supabase error updating record for {image_id}: {update_response.error}")
                elif not update_response.data:
                    print(f"  -> No record found for image_id '{image_id}' in ham_metadata table.")
                else:
                    print(f"  -> Supabase reports successful update for {image_id}.")
                    
                    # Verification step
                    try:
                        verify_response = supabase.table('ham_metadata').select('embedding').eq('image_id', image_id).execute()
                        if verify_response.data and verify_response.data[0].get('embedding') is not None:
                            print(f"  -> VERIFIED: Embedding is present for {image_id}.")
                        else:
                            print(f"  -> VERIFICATION FAILED: Embedding is NULL for {image_id} after update.")
                    except Exception as e:
                        print(f"  -> Error during verification for {image_id}: {e}")

            except Exception as e:
                print(f"  -> An error occurred while updating the database for {image_id}: {e}")

        print("\nEmbedding population script finished.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Load environment variables from a .env file in the project root
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
        print(f"Loaded .env file from {dotenv_path}")
    else:
        print(".env file not found at project root, relying on environment variables.")
        
    populate_embeddings()
