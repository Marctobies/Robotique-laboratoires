# Auteur: Marc-Antoine Faucher et Loik Boulanger
# Date: 2025-11-17

from ia import IA
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader


def main():
    print("\n" + "=" * 60)
    print("ENTRAÎNEMENT DU MODÈLE DE DÉTECTION D'OBSTACLES")
    print("=" * 60 + "\n")
    
    ia = IA()
    
    ia.entrainer(
        dataset_path="dataset",
        num_epochs=10,
        learning_rate=0.001,
        batch_size=32
    )
    
    accuracy = ia.evaluer(dataset_path="dataset")
    
    ia.sauvegarder("modele_obstacle.pt")
    
    print("\n" + "=" * 60)
    print("PROCESSUS TERMINÉ")
    print("=" * 60)
  

if __name__ == "__main__":
    main()