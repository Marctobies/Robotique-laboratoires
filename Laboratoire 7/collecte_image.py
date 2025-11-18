# Auteur: Marc-Antoine Faucher et Loik Boulanger
# Date: 2025-11-17

import cv2
from camera import Camera
from robot import Robot
import os

def main():
    camera = Camera()
    robot = Robot()
    
    compteur_obstacle = 1
    compteur_libre = 1
    
    dossier_obstacle = "obstacles"
    dossier_libre = "libres"
    
    try:
        while True:
            frame = camera.capturer_image()
            
            texte = f"Obstacles: {compteur_obstacle-1} | Libres: {compteur_libre-1}"
            cv2.putText(frame, texte, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            camera.afficher_image(frame, "Collecte d'images - Appuyez sur O ou L")
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('w'):
                robot.avancer()
            elif key == ord('s'):
                robot.reculer()
            elif key == ord('a'):
                robot.tourner_gauche()
            elif key == ord('d'):
                robot.tourner_droite()
            elif key == ord(' '):
                robot.arreter()
            
            elif key == ord('o'):
                nom_fichier = f"obstacle_{compteur_obstacle:03d}.jpg"
                chemin = camera.sauvegarder_image(dossier_obstacle, nom_fichier)
                print(f"✓ Sauvegardé: {chemin}")
                compteur_obstacle += 1
            
            elif key == ord('l'):
                nom_fichier = f"libre_{compteur_libre:03d}.jpg"
                chemin = camera.sauvegarder_image(dossier_libre, nom_fichier)
                print(f"✓ Sauvegardé: {chemin}")
                compteur_libre += 1
            
            elif key == 27:  
                break
    
    finally:
        robot.arreter()
        camera.release()
        
        print(f"Collecte terminée!")
        print(f"  Images obstacles: {compteur_obstacle-1}")
        print(f"  Images libres: {compteur_libre-1}")
        print(f"  Total: {compteur_obstacle + compteur_libre - 2}")
      

if __name__ == "__main__":
    main()