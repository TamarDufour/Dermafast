import pandas as pd
import os

def create_non_training_set():
    """
    This script creates a CSV file containing image_ids from HAM10000_metadata.csv
    that were not used for training a model.

    The training set is defined as the images in HAM10000_binary_balanced.csv
    minus the images in test_images_ids.csv.

    The final set of images are all images from HAM10000_metadata.csv minus the
    training set.
    """
    # Relative paths from the script's location in backend/scripts/
    scripts_dir = os.path.dirname(__file__)
    moles_data_dir = os.path.join(scripts_dir, '../../moles_data/')
    output_dir = scripts_dir

    # File paths
    binary_balanced_path = os.path.join(moles_data_dir, 'HAM10000_binary_balanced.csv')
    test_ids_path = os.path.join(moles_data_dir, 'test_images_ids.csv')
    metadata_path = os.path.join(moles_data_dir, 'HAM10000_metadata.csv')
    output_path = os.path.join(output_dir, 'non_training_moles.csv')

    # Read the CSV files
    try:
        binary_balanced_df = pd.read_csv(binary_balanced_path)
        test_ids_df = pd.read_csv(test_ids_path)
        metadata_df = pd.read_csv(metadata_path)
    except FileNotFoundError as e:
        print(f"Error reading files: {e}")
        return

    # Get the image_id sets
    balanced_ids = set(binary_balanced_df['image_id'])
    test_ids = set(test_ids_df['image_id'])
    all_metadata_ids = set(metadata_df['image_id'])

    # Determine training and non-training IDs
    training_ids = balanced_ids - test_ids
    non_training_ids = all_metadata_ids - training_ids

    # Create the output DataFrame
    non_training_df = pd.DataFrame(list(non_training_ids), columns=['image_id'])

    # Save to CSV
    non_training_df.to_csv(output_path, index=False)

    print(f"Successfully created {output_path} with {len(non_training_df)} non-training image IDs.")

if __name__ == "__main__":
    create_non_training_set()

