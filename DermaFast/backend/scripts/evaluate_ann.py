import os
import sys
import pandas as pd
import numpy as np
import asyncio
from dotenv import load_dotenv

# Add project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.app.ml_model import load_model, inference
from backend.app.faiss_service import faiss_service

async def evaluate_ann():
    """
    Evaluates the ANN embeddings by calculating precision@9 and recall@9.
    """
    print("Starting ANN evaluation script...")

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))

    # Load the model and FAISS service
    print("Loading model...")
    model = load_model()
    print("Model loaded.")

    # Load embeddings into FAISS
    print("Loading embeddings into FAISS service...")
    await faiss_service.load_embeddings()
    if not faiss_service.embeddings_loaded:
        print("Failed to load embeddings. Exiting.")
        return
    print("Embeddings loaded into FAISS.")

    # Load test data and metadata
    print("Loading test data and metadata...")
    test_moles_df = pd.read_csv(os.path.join(script_dir, 'non_training_moles.csv'))
    metadata_df = pd.read_csv(os.path.join(project_root, 'moles_data', 'HAM10000_metadata.csv'))
    
    # Create a mapping from image_id to diagnosis for quick lookup
    image_id_to_dx = pd.Series(metadata_df.dx.values, index=metadata_df.image_id).to_dict()
    
    print(f"Loaded {len(test_moles_df)} test images and {len(metadata_df)} metadata records.")

    precisions = []
    not_found_images = []
    results_by_dx = {}
    at_least_3_matches_count = 0
    at_least_5_matches_count = 0
    at_least_6_matches_count = 0
    at_least_8_matches_count = 0
    zero_matches_count = 0
    processed_count = 0

    non_melanoma_group_results = {
        'precisions': [], 'count': 0, 'at_least_3_matches': 0,
        'at_least_5_matches': 0, 'at_least_6_matches': 0,
        'at_least_8_matches': 0, 'zero_matches': 0
    }

    k = 9

    for index, row in test_moles_df.iterrows():
        query_image_id = row['image_id']
        
        image_path_1 = os.path.join(project_root, f'moles_data/HAM10000_images_part_1/{query_image_id}.jpg')
        image_path_2 = os.path.join(project_root, f'moles_data/HAM10000_images_part_2/{query_image_id}.jpg')
        
        image_path = None
        if os.path.exists(image_path_1):
            image_path = image_path_1
        elif os.path.exists(image_path_2):
            image_path = image_path_2
        else:
            not_found_images.append(query_image_id)
            continue
            
        print(f"\nProcessing {query_image_id}...")

        # Get ground truth diagnosis
        if query_image_id not in image_id_to_dx:
            print(f"Warning: No metadata found for {query_image_id}. Skipping.")
            continue
        query_dx = image_id_to_dx[query_image_id]
        processed_count += 1

        # Read image and get embedding
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        _, embedding = inference(model, image_bytes)

        # Find similar images (request k+1 because the image itself will be in the results)
        similar_results = await faiss_service.find_similar_images(embedding, k=k + 1)
        
        # Exclude the query image itself from the results
        retrieved_ids = [img_id for img_id, dist in similar_results if img_id != query_image_id][:k]
        
        if len(retrieved_ids) != k:
             print(f"Warning: Expected {k} results for {query_image_id}, but got {len(retrieved_ids)}.")

        # Calculate true positives
        true_positives = sum(1 for res_id in retrieved_ids if image_id_to_dx.get(res_id) == query_dx)

        if true_positives >= 3:
            at_least_3_matches_count += 1
        if true_positives >= 5:
            at_least_5_matches_count += 1
        if true_positives >= 6:
            at_least_6_matches_count += 1
        if true_positives >= 8:
            at_least_8_matches_count += 1
        if true_positives == 0:
            zero_matches_count += 1

        # Calculate Precision@k
        precision_at_k = true_positives / k
        precisions.append(precision_at_k)

        # Store results by dx
        if query_dx not in results_by_dx:
            results_by_dx[query_dx] = {'precisions': [], 'count': 0, 'at_least_3_matches': 0, 'at_least_5_matches': 0, 'at_least_6_matches': 0, 'at_least_8_matches': 0, 'zero_matches': 0}
        results_by_dx[query_dx]['precisions'].append(precision_at_k)
        results_by_dx[query_dx]['count'] += 1
        if true_positives >= 3:
            results_by_dx[query_dx]['at_least_3_matches'] += 1
        if true_positives >= 5:
            results_by_dx[query_dx]['at_least_5_matches'] += 1
        if true_positives >= 6:
            results_by_dx[query_dx]['at_least_6_matches'] += 1
        if true_positives >= 8:
            results_by_dx[query_dx]['at_least_8_matches'] += 1
        if true_positives == 0:
            results_by_dx[query_dx]['zero_matches'] += 1

        # For non-melanoma images, calculate binary performance (any non-melanoma is a match)
        if query_dx != 'mel':
            binary_true_positives = sum(1 for res_id in retrieved_ids if image_id_to_dx.get(res_id) != 'mel')
            
            non_melanoma_group_results['count'] += 1
            precision_at_k_binary = binary_true_positives / k
            non_melanoma_group_results['precisions'].append(precision_at_k_binary)

            if binary_true_positives >= 3:
                non_melanoma_group_results['at_least_3_matches'] += 1
            if binary_true_positives >= 5:
                non_melanoma_group_results['at_least_5_matches'] += 1
            if binary_true_positives >= 6:
                non_melanoma_group_results['at_least_6_matches'] += 1
            if binary_true_positives >= 8:
                non_melanoma_group_results['at_least_8_matches'] += 1
            if binary_true_positives == 0:
                non_melanoma_group_results['zero_matches'] += 1

        print(f"  -> Query diagnosis: {query_dx}")
        print(f"  -> Found {true_positives}/{k} similar moles with the same diagnosis.")
        print(f"  -> Precision@{k}: {precision_at_k:.4f}")

    # Calculate and print average metrics
    avg_precision = np.mean(precisions) if precisions else 0
    percent_at_least_3_matches = (at_least_3_matches_count / processed_count * 100) if processed_count > 0 else 0
    percent_at_least_5_matches = (at_least_5_matches_count / processed_count * 100) if processed_count > 0 else 0
    percent_at_least_6_matches = (at_least_6_matches_count / processed_count * 100) if processed_count > 0 else 0
    percent_at_least_8_matches = (at_least_8_matches_count / processed_count * 100) if processed_count > 0 else 0
    percent_zero_matches = (zero_matches_count / processed_count * 100) if processed_count > 0 else 0

    # --- Calculate final non-melanoma group metrics ---
    if non_melanoma_group_results['count'] > 0:
        avg_precision_nm = np.mean(non_melanoma_group_results['precisions'])
        count_nm = non_melanoma_group_results['count']
        percent_at_least_3_nm = (non_melanoma_group_results['at_least_3_matches'] / count_nm * 100)
        percent_at_least_5_nm = (non_melanoma_group_results['at_least_5_matches'] / count_nm * 100)
        percent_at_least_6_nm = (non_melanoma_group_results['at_least_6_matches'] / count_nm * 100)
        percent_at_least_8_nm = (non_melanoma_group_results['at_least_8_matches'] / count_nm * 100)
        percent_zero_nm = (non_melanoma_group_results['zero_matches'] / count_nm * 100)


    # --- Output results to a file ---
    results_dir = os.path.join(script_dir, 'results')
    os.makedirs(results_dir, exist_ok=True)
    results_file_path = os.path.join(results_dir, 'ann_evaluation_results.txt')

    with open(results_file_path, 'w') as f:
        f.write("--- Evaluation Summary ---\n")
        f.write(f"Processed {processed_count} test images.\n")
        f.write(f"Average Precision@{k}: {avg_precision:.4f}\n")
        f.write(f"% with at least 3/9 correct diagnoses: {percent_at_least_3_matches:.2f}%\n")
        f.write(f"% with at least 5/9 correct diagnoses: {percent_at_least_5_matches:.2f}%\n")
        f.write(f"% with at least 6/9 correct diagnoses: {percent_at_least_6_matches:.2f}%\n")
        f.write(f"% with at least 8/9 correct diagnoses: {percent_at_least_8_matches:.2f}%\n")
        f.write(f"% with no correct diagnoses: {percent_zero_matches:.2f}%\n")
        f.write("--------------------------\n")

        if not_found_images:
            f.write("\n--- Images Not Found ---\n")
            for image_id in sorted(not_found_images):
                f.write(f"  - {image_id}\n")
            f.write("--------------------------\n")

        f.write("\n--- Results by Diagnosis ---\n")
        # Add non-melanoma to the list of diagnoses to print, but handle it separately
        sorted_dx = sorted(results_by_dx.items())
        
        for dx, data in sorted_dx:
            avg_precision_dx = np.mean(data['precisions'])
            count = data['count']
            percent_at_least_3_dx = (data['at_least_3_matches'] / count * 100) if count > 0 else 0
            percent_at_least_5_dx = (data['at_least_5_matches'] / count * 100) if count > 0 else 0
            percent_at_least_6_dx = (data['at_least_6_matches'] / count * 100) if count > 0 else 0
            percent_at_least_8_dx = (data['at_least_8_matches'] / count * 100) if count > 0 else 0
            percent_zero_dx = (data['zero_matches'] / count * 100) if count > 0 else 0

            f.write(f"\nDiagnosis: {dx} ({count} samples)\n")
            f.write(f"  - Avg Precision@{k}: {avg_precision_dx:.4f}\n")
            f.write(f"  - % with at least 3/9 correct: {percent_at_least_3_dx:.2f}%\n")
            f.write(f"  - % with at least 5/9 correct: {percent_at_least_5_dx:.2f}%\n")
            f.write(f"  - % with at least 6/9 correct: {percent_at_least_6_dx:.2f}%\n")
            f.write(f"  - % with at least 8/9 correct: {percent_at_least_8_dx:.2f}%\n")
            f.write(f"  - % with no correct diagnoses: {percent_zero_dx:.2f}%\n")
        
        # --- Write non-melanoma group results to file ---
        if non_melanoma_group_results['count'] > 0:
            f.write(f"\nDiagnosis: non-melanoma ({count_nm} samples) [binary classification]\n")
            f.write(f"  - Avg Precision@{k}: {avg_precision_nm:.4f}\n")
            f.write(f"  - % with at least 3/9 correct: {percent_at_least_3_nm:.2f}%\n")
            f.write(f"  - % with at least 5/9 correct: {percent_at_least_5_nm:.2f}%\n")
            f.write(f"  - % with at least 6/9 correct: {percent_at_least_6_nm:.2f}%\n")
            f.write(f"  - % with at least 8/9 correct: {percent_at_least_8_nm:.2f}%\n")
            f.write(f"  - % with no correct diagnoses: {percent_zero_nm:.2f}%\n")

        f.write("----------------------------\n")

    print(f"\nResults have been saved to {results_file_path}")


    print("\n--- Evaluation Summary ---")
    print(f"Processed {processed_count} test images.")
    print(f"Average Precision@{k}: {avg_precision:.4f}")
    print(f"% with at least 3/9 correct diagnoses: {percent_at_least_3_matches:.2f}%")
    print(f"% with at least 5/9 correct diagnoses: {percent_at_least_5_matches:.2f}%")
    print(f"% with at least 6/9 correct diagnoses: {percent_at_least_6_matches:.2f}%")
    print(f"% with at least 8/9 correct diagnoses: {percent_at_least_8_matches:.2f}%")
    print(f"% with no correct diagnoses: {percent_zero_matches:.2f}%")
    print("--------------------------")

    if not_found_images:
        print("\n--- Images Not Found ---")
        for image_id in sorted(not_found_images):
            print(f"  - {image_id}")
        print("--------------------------")

    print("\n--- Results by Diagnosis ---")
    # Add non-melanoma to the list of diagnoses to print, but handle it separately
    sorted_dx = sorted(results_by_dx.items())
    
    for dx, data in sorted_dx:
        avg_precision_dx = np.mean(data['precisions'])
        count = data['count']
        percent_at_least_3_dx = (data['at_least_3_matches'] / count * 100) if count > 0 else 0
        percent_at_least_5_dx = (data['at_least_5_matches'] / count * 100) if count > 0 else 0
        percent_at_least_6_dx = (data['at_least_6_matches'] / count * 100) if count > 0 else 0
        percent_at_least_8_dx = (data['at_least_8_matches'] / count * 100) if count > 0 else 0
        percent_zero_dx = (data['zero_matches'] / count * 100) if count > 0 else 0

        print(f"\nDiagnosis: {dx} ({count} samples)")
        print(f"  - Avg Precision@{k}: {avg_precision_dx:.4f}")
        print(f"  - % with at least 3/9 correct: {percent_at_least_3_dx:.2f}%")
        print(f"  - % with at least 5/9 correct: {percent_at_least_5_dx:.2f}%")
        print(f"  - % with at least 6/9 correct: {percent_at_least_6_dx:.2f}%")
        print(f"  - % with at least 8/9 correct: {percent_at_least_8_dx:.2f}%")
        print(f"  - % with no correct diagnoses: {percent_zero_dx:.2f}%")
    
    # --- Print non-melanoma group results to console ---
    if non_melanoma_group_results['count'] > 0:
        print(f"\nDiagnosis: non-melanoma ({count_nm} samples) [binary classification]")
        print(f"  - Avg Precision@{k}: {avg_precision_nm:.4f}")
        print(f"  - % with at least 3/9 correct: {percent_at_least_3_nm:.2f}%")
        print(f"  - % with at least 5/9 correct: {percent_at_least_5_nm:.2f}%")
        print(f"  - % with at least 6/9 correct: {percent_at_least_6_nm:.2f}%")
        print(f"  - % with at least 8/9 correct: {percent_at_least_8_nm:.2f}%")
        print(f"  - % with no correct diagnoses: {percent_zero_nm:.2f}%")

    print("----------------------------")
    if os.path.exists(results_file_path):
        print(f"\nResults have been saved to {results_file_path}")


if __name__ == "__main__":
    dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path=dotenv_path)
        print(f"Loaded .env file from {dotenv_path}")
    else:
        print(".env file not found at project root, relying on environment variables.")
        
    asyncio.run(evaluate_ann())
