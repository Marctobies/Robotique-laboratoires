# Auteur: Marc-Antoine Faucher et Loik Boulanger
# Date: 2025-11-17

import cv2
from camera import Camera
from robot import Robot
from ia import IA

def main():
    print("Initialisation du système...")
    camera = Camera()
    robot = Robot()
    ia = IA()
    
    try:
        ia.charger("modele_obstacle.pt")
    except FileNotFoundError:
        print("ERREUR: Fichier 'modele_obstacle.pt' introuvable!")
        print("Veuillez transférer le modèle entraîné depuis votre laptop.")
        return
    
 
    
    obstacle_detecte = False
    
    try:
        while True:
            # Capturer l'image
            frame = camera.capturer_image()
            
            # Prédire avec l'IA
            obstacle_detecte, label, confiance = ia.predire(frame)
            
            # Affichage de l'état sur l'image
            if obstacle_detecte:
                # OBSTACLE DÉTECTÉ - Affichage en rouge
                texte = f"OBSTACLE DÉTECTÉ! ({confiance*100:.1f}%)"
                couleur = (0, 0, 255)  # Rouge en BGR
                cv2.rectangle(frame, (0, 0), (frame.shape[1], 80), (0, 0, 200), -1)
                cv2.putText(frame, texte, (10, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1.2, couleur, 3)
            else:
                # VOIE LIBRE - Affichage en vert
                texte = f"VOIE LIBRE ({confiance*100:.1f}%)"
                couleur = (0, 255, 0)
                cv2.putText(frame, texte, (10, 40), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, couleur, 2)
            
            # Afficher l'image
            camera.afficher_image(frame, "Détection d'obstacles")
            
            # Lire la touche
            key = cv2.waitKey(1) & 0xFF
            
            # Gestion des commandes
            if key == ord('w'):
                if obstacle_detecte:
                    print("AVANCER BLOQUÉ - Obstacle détecté!")
                    robot.arreter()
                else:
                    robot.avancer()
            
            elif key == ord('s'):
                robot.reculer()
            
            elif key == ord('a'):
                robot.tourner_gauche()

            elif key == ord('q'):
                robot.tourner_gauche_leger()

            elif key == ord('d'):
                robot.tourner_droite()

            elif key == ord('e'):
                robot.tourner_droite_leger()

            elif key == ord('x'):
                robot.arreter()
                break
    
    finally:
        robot.arreter()
        camera.release()
        print("\nSystème arrêté.")

if __name__ == "__main__":
    main()