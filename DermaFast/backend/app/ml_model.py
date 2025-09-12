import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import io

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

def load_model(model_path='model.pth'):
    model = BasicCNN()
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model

def inference(model: nn.Module, image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image_tensor = val_transform(image).unsqueeze(0)

    with torch.no_grad():
        classification, embedding = model(image_tensor)
        
    return classification.item(), embedding.numpy().flatten().tolist()
