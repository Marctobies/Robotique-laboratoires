# Auteur: Marc-Antoine Faucher et Loik Boulanger
# Date: 2025-11-20

# J'ai fait un fichier séparé qui utilise la classe IA pour entraîner le modèle.
# Cela me permet d'afficher des messages spécifiques à l'entraînement pour tester et déboguer plus facilement
# sans encombrer ma méthode dans la classe IA.


from ia import IA
import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader


def main():

    print("Début de l'entraînement du modèle")
    
    ia = IA()
    
    ia.entrainer(
        dataset_path="dataset",
        num_epochs=10,
        learning_rate=0.001,
        batch_size=32
    )
    
    accuracy = ia.evaluer(dataset_path="dataset")
    
    ia.sauvegarder("modele_obstacle.pt")
    
    print("Entraînement terminé")
  

if __name__ == "__main__":
    main()