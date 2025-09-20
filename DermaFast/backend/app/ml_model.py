import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import io
import os

# Image transformation
val_transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

# CNN Model Definition
class BasicCNN(nn.Module):
    def __init__(self):
        super(BasicCNN, self).__init__()

        # First convolutional layer: input = 3 channels (RGB), output = 16 filters
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=3, padding=1)

        # Max pooling to reduce spatial dimensions
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        # Second convolutional layer: input = 16, output = 32 filters
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1)

        # Fully connected layer: expects flattened input of size 32*64*64
        self.fc1 = nn.Linear(32 * 64 * 64, 256)

        self.dropout = nn.Dropout(p=0.3)  # Dropout with 30% drop rate

        # Final layer: outputs a single probability for binary classification
        self.fc2 = nn.Linear(256, 1)

    def forward(self, x):
        # Conv -> ReLU -> Pool
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))

        # Flatten the tensor
        x = x.view(-1, 32 * 64 * 64)

        # Fully connected layers
        x = F.relu(self.fc1(x))
        embedding = self.dropout(x)
        
        # Get classification result
        classification = torch.sigmoid(self.fc2(embedding))
        
        return classification, embedding

def load_model():
    """
    Load the pre-trained model from the specified path.
    """
    try:
        # Get the absolute path to the directory of the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Construct the absolute path to the model weights, assuming the script is in backend/app/
        model_path = os.path.join(script_dir, 'ml_model', 'model_weights.pkl')
        
        print(f"Loading model from: {model_path}")

        # Check if the file exists before attempting to load
        if not os.path.exists(model_path):
            # Fallback for when script is run from a different structure, e.g. tests
            app_dir = os.path.join(os.path.dirname(script_dir), "app")
            model_path = os.path.join(app_dir, 'ml_model', 'model_weights.pkl')
            print(f"Fallback: Loading model from: {model_path}")
            if not os.path.exists(model_path):
                 raise FileNotFoundError(f"Model file not found at: {model_path}")

        model = BasicCNN()
        # The state dict is loaded from a pickled file, not directly from .pth
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        model.eval()  # Set the model to evaluation mode
        print("Model loaded successfully.")
        return model
    except FileNotFoundError as e:
        print(f"Error loading model from {model_path}: {e}")
        raise e
    except Exception as e:
        # General exception for other potential errors (e.g., torch issues)
        print(f"An unexpected error occurred while loading the model: {e}")
        raise e

def inference(model: nn.Module, image_bytes: bytes):
    """
    Perform inference on a mole image.
    
    Args:
        model: The loaded BasicCNN model
        image_bytes: Raw image data as bytes
        
    Returns:
        Tuple of (classification_probability, embedding_list)
        
    TODO: Currently, there is no threshold for the classification, we will need to add it later.
    As the results are stored in the database, we'll be able to adjust the results later.
    """
    try:
        # Load and convert image
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Transform image
        image_tensor = val_transform(image).unsqueeze(0)

        with torch.no_grad():
            classification, embedding = model(image_tensor)
            
        return classification.item(), embedding.numpy().flatten().tolist()
        
    except Exception as e:
        print(f"Error in inference: {str(e)}")
        raise e
