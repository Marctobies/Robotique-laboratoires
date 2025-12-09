# Auteur: Marc-Antoine Faucher et Loik Boulanger
# Date: 2025-11-20

import cv2
from camera import Camera
from robot import Robot
from ia import IA

def main():
    print("Démarrage du système de détection d'obstacles")
    camera = Camera()
    robot = Robot()
    ia = IA()

    try:
        ia.charger("modele_obstacle.pt")
    except FileNotFoundError:
        print("Erreur: Fichier du modèle introuvable")
        return

    window_name = "Détection d'obstacles"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    
    SEUIL_CONFIANCE = 0.95

    
    try:
        key = cv2.waitKey(1) 
        while key != ord('x') :
            frame = camera.capturer_image()

            is_obstacle, label, confiance = ia.predire(frame)

            if is_obstacle and confiance < SEUIL_CONFIANCE:
                is_obstacle = False

            if is_obstacle:
                texte = f"OBSTACLE ! ({confiance * 100:.1f}%)"
                couleur = (0, 0, 255)
                cv2.rectangle(frame, (0, 0), (frame.shape[1], 80), (0, 0, 200), -1)
                cv2.putText(frame, texte, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, couleur, 3)

                robot.arreter()

            else:
                texte = f"VOIE LIBRE ! ({confiance * 100:.1f}%)"
                couleur = (0, 255, 0)
                cv2.putText(frame, texte, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, couleur, 2)

            cv2.imshow(window_name, frame)
            
            if key == ord('w'):
                if not is_obstacle:
                    robot.avancer()
                else:
                    print("Obstacle détecté")

            elif key == ord('s'):
                robot.reculer()

            elif key == ord('a'):
                robot.tourner_gauche()

            elif key == ord('d'):
                robot.tourner_droite()

            elif key == ord(' ') or key == ord('x'):
                robot.arreter()

            elif key == ord('x'):
                robot.arreter()
                break
    finally:
        robot.arreter()
        camera.release()
        cv2.destroyAllWindows()
        print("\nSystème arrêté.")

if __name__ == "__main__":
    main()