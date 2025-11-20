# Auteur: Marc-Antoine Faucher et Loik Boulanger
# Date: 2025-11-06

import time
from robot import Robot
from orientation import Orientation

from robot import *
from orientation import *

if __name__ == "__main__":
    robot = Robot()
    orientation = Orientation()

robot = Robot()
orientation = Orientation()
print("Début du programme. Le robot est immobile, calcul du biais en cours...")
print("Laissez le robot immobile pendant environ 5 secondes.")
time.sleep(5)

orientation_actuel = orientation.imu
print(orientation_actuel)
# Simuler un mouvement
print("\nLe robot est maintenant considéré 'en mouvement'.")
orientation.en_mouvement = True

try:
    # Boucle principale pour afficher les données
    for _ in range(100): # Affiche les données pendant 20 secondes (200 * 0.1s)
        with orientation._lock: # Utilise le verrou pour un accès sécurisé
            angle_relatif = orientation.angle_x_relatif
            cap = orientation.cap_magnetique
            biais = orientation.biais_gx

        print(f"Angle X Relatif: {angle_relatif:.2f}° | Cap Magnétique: {cap:.2f}° | Biais Gx: {biais:.4f}")
        time.sleep(0.1)

finally:
    print("\nArrêt du programme.")
    orientation.arreter()   
