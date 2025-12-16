#Etienne La Rochelle
#2025-11-17

import torch.nn as nn
import torch.optim as optim
import os
import torch
import cv2
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

class IA:

    NUM_CLASSES = 2
    CHEMIN_MODELE = "mon_model.pt"

    def __init__(self):
        self.modele = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(32 * 32 * 32, 128),
            nn.ReLU(),
            nn.Linear(128, self.NUM_CLASSES)
        )
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def preparer_images(self, mode):
        dataset_path="dataset"
        batch_size=32
        transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(), ])
        mode_actuel = datasets.ImageFolder(os.path.join(dataset_path, mode), transform=transform)
        return DataLoader(mode_actuel, batch_size, shuffle=True)


    def entrainement_images(self):
        print("Début de l'entrainement...")
        train_loader = self.preparer_images('train')

        num_epochs=10
        learning_rate=0.001
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.modele.parameters(), lr=learning_rate)
        self.modele.to(self.device)
        self.modele.train()
        for epoch in range(num_epochs):
            total_loss, correct = 0, 0
            for images, labels in train_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.modele(images)
                loss = criterion(outputs, labels)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
                correct += (outputs.argmax(1) == labels).sum().item()
            acc = 100 * correct / len(train_loader.dataset)
            print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}, Accuracy: {acc:.2f}%")
        print("Entrainement terminé.")


    def evaluation_images(self):
        print("Début de l'évaluation...")
        val_loader = self.preparer_images('val')

        self.modele.eval()
        correct = 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.modele(images)
                correct += (outputs.argmax(1) == labels).sum().item() 
        acc = 100 * correct / len(val_loader.dataset) 
        print(f"Accuracy: {acc:.2f}%")
        print("Évaluation terminé.")


    def trouver_obstacle(self, frame):
        self.modele.eval()
        frame_resized = cv2.resize(frame, (128, 128))
        image = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        image = torch.tensor(image.transpose(2, 0, 1)).float().unsqueeze(0) / 255.0
        image = image.to(self.device)
        with torch.no_grad():
            output = self.modele(image)
            _, predicted = torch.max(output, 1)
        return predicted.item()


    def sauvegarder_modele(self, param_seulement=False):
        if param_seulement:
            torch.save(self.modele.state_dict(), self.CHEMIN_MODELE)
        else:
            torch.save(self.modele, self.CHEMIN_MODELE)

    
    def charger_modele(self, param_seulement=False):
        if param_seulement:
            self.modele.load_state_dict(torch.load(self.CHEMIN_MODELE, map_location=self.device, weights_only=False))
        else:
            self.modele = torch.load(self.CHEMIN_MODELE, map_location=self.device, weights_only=False)
