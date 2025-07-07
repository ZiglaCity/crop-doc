import torch
from torchvision import models, transforms
from PIL import Image
import os
import requests
import torch.nn as nn

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class SimpleCNN(nn.Module):
    def __init__(self, num_classes):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 56 * 56, 256)
        self.fc2 = nn.Linear(256, num_classes)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))   # -> (32, 112, 112)
        x = self.pool(self.relu(self.conv2(x)))   # -> (64, 56, 56)
        x = x.view(x.size(0), -1)                 # Flatten
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

class_labels = [
    'Cassava - bacterial blight', 'Cassava - brown spot', 'Cassava - green mite', 'Cassava - healthy', 'Cassava - mosaic',
    'Maize - leaf spot', 'Maize - leaf blight', 'Maize - fall armyworm', 'Maize - grasshoper', 'Maize - streak virus',
    'Maize - leaf beetle', 'Maize - healthy',
    'Tomato - leaf curl', 'Tomato - leaf blight', 'Tomato - septoria leaf spot', 'Tomato - verticulium wilt', 'Tomato - healthy',
    'Cashew - gumosis', 'Cashew - red rust', 'Cashew - anthracnose', 'Cashew - leaf miner', 'Cashew - healthy'
]

MODEL_PATH = 'models/best_model_v1_75percent.pth'
MODEL_ = 'https://github.com/steveAzo/ccmt-api/releases/tag/v1.0'
MODEL_URL = 'https://github.com/steveAzo/ccmt-api/releases/download/v1.0/best_model_v1_71percent.pth'


def download_model():
    print("Attempting to download...")
    state_dict = torch.load(MODEL_PATH, map_location='cpu')
    print(state_dict.keys())
    if not os.path.exists('models'):
        print("Model does not exist...")
        os.makedirs('models')
    if not os.path.isfile(MODEL_PATH):
        print("Downloading model...")
        response = requests.get(MODEL_URL)
        with open(MODEL_PATH, 'wb') as f:
            f.write(response.content)
        print("Model downloaded successfully!")

def load_model():
    download_model()
    print("Hey I attempted to download the model, and it's probably done...")
    model = SimpleCNN(num_classes=7)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    model.to(device)
    model.eval()
    return model, class_labels


def predict_image(image: Image.Image, model, class_labels):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
        confidence, predicted_idx = torch.max(probabilities, dim=0)
        predicted_label = class_labels[predicted_idx.item()]

    return predicted_label, round(confidence.item(), 4)
