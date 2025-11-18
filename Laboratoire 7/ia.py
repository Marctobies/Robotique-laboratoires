# Auteur: Marc-Antoine Faucher et Loik Boulanger
# Date: 2025-11-17

import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import cv2
import numpy as np

#Référence pour CUDA: https://docs.pytorch.org/docs/stable/cuda.html
class IA:
    def __init__(self):
        self.num_classes = 2
        # J'utilise ici les CUDA core de mon GPU plutôt que mon processeur pour accélérer les calculs.
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Device utilisé: {self.device}")
        
        # Créer le modèle
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
            nn.Linear(128, self.num_classes)
        )
        
        self.modele.to(self.device)
        
        self.labels = ["libres", "obstacles"]
    
    def entrainer(self, dataset_path="dataset", num_epochs=10, learning_rate=0.001, batch_size=32):
        
        print("\n" + "=" * 60)
        print("ENTRAÎNEMENT DU MODÈLE")
        print("=" * 60)
        
        transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
        ])
        
        train_path = os.path.join(dataset_path, "train")
        train_dataset = datasets.ImageFolder(train_path, transform=transform)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        
        print(f"\nDataset d'entraînement:")
        print(f"  Nombre d'images: {len(train_dataset)}")
        print(f"  Classes: {train_dataset.classes}")
        print(f"  Batch size: {batch_size}")
        print(f"  Nombre de batches: {len(train_loader)}")
        
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.modele.parameters(), lr=learning_rate)
        
        self.modele.train()
        
        print(f"\nParamètres d'entraînement:")
        print(f"  Epochs: {num_epochs}")
        print(f"  Learning rate: {learning_rate}")
        print(f"  Device: {self.device}")
        print("\n" + "-" * 60)
        
        for epoch in range(num_epochs):
            total_loss = 0
            correct = 0
            
            for images, labels in train_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                
                outputs = self.modele(images)
                loss = criterion(outputs, labels)
                
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
                correct += (outputs.argmax(1) == labels).sum().item()
            
            accuracy = 100 * correct / len(train_dataset)
            avg_loss = total_loss / len(train_loader)
            
            print(f"Epoch {epoch+1}/{num_epochs} - Loss: {avg_loss:.4f} - Accuracy: {accuracy:.2f}%")
        
        print("-" * 60)
        print("✓ Entraînement terminé!")
        print("=" * 60 + "\n")
    
    def evaluer(self, dataset_path="dataset"):
        
        print("\n" + "=" * 60)
        print("ÉVALUATION DU MODÈLE")
        print("=" * 60)
        
        transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
        ])
        
        val_path = os.path.join(dataset_path, "val")
        val_dataset = datasets.ImageFolder(val_path, transform=transform)
        val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
        
        print(f"\nDataset de validation:")
        print(f"  Nombre d'images: {len(val_dataset)}")
        print(f"  Classes: {val_dataset.classes}")
        
        self.modele.eval()
        
        correct = 0
        total = 0
        
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.modele(images)
                correct += (outputs.argmax(1) == labels).sum().item()
                total += labels.size(0)
        
        accuracy = 100 * correct / total
        
        print(f"\n{'Résultat:'}")
        print(f"Accuracy: {accuracy:.2f}%")
        print(f"Images correctes: {correct}/{total}")
        
        if accuracy >= 85:
            print("Excellente performance!")
        elif accuracy >= 70:
            print("Performance acceptable mais peut être améliorée")
        else:
            print("Performance faible - collectez plus d'images variées")
        
        print("=" * 60 + "\n")
        
        return accuracy
    
    def predire(self, image):
       
        self.modele.eval()
        
        frame_resized = cv2.resize(image, (128, 128))
        image_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        
        image_tensor = torch.tensor(image_rgb.transpose(2, 0, 1)).float().unsqueeze(0) / 255.0
        image_tensor = image_tensor.to(self.device)
        
        with torch.no_grad():
            output = self.modele(image_tensor)
            probabilities = torch.softmax(output, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
        
        label_index = predicted.item()
        label = self.labels[label_index]
        confidence_value = confidence.item()
        
        obstacle_detecte = (label == "obstacles")
        
        return obstacle_detecte, label, confidence_value
    
    def sauvegarder(self, chemin="modele_obstacle.pt"):
        torch.save(self.modele.state_dict(), chemin)
        print(f"Modèle sauvegardé: {chemin}")
    
    def charger(self, chemin="modele_obstacle.pt"):
        self.modele.load_state_dict(torch.load(chemin, map_location=self.device))
        self.modele.to(self.device)
        print(f"Modèle chargé: {chemin}")