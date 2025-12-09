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

    # Créer la fenêtre une seule fois, avant la boucle
    window_name = "Détection d'obstacles"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    # Définir un seuil de sécurité (80%)
    SEUIL_CONFIANCE = 0.95

    try:
        while True:
            frame = camera.capturer_image()

            is_obstacle, label, confiance = ia.predire(frame)

            if is_obstacle and confiance < SEUIL_CONFIANCE:
                is_obstacle = False
                texte_debug = f"Ignoré ({confiance * 100:.1f}%)"

            if is_obstacle:
                texte = f"OBSTACLE ! ({confiance * 100:.1f}%)"
                couleur = (0, 0, 255)
                cv2.rectangle(frame, (0, 0), (frame.shape[1], 80), (0, 0, 200), -1)
                cv2.putText(frame, texte, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, couleur, 3)
                key = cv2.waitKey(1) & 0xFF

                if key == ord('w'):
                    if not is_obstacle:
                        robot.avancer()
                    else:
                        print("COMMANDE REFUSÉE : Obstacle devant !")

                elif key == ord('s'):
                    robot.reculer()

                elif key == ord('a'):
                    robot.tourner_gauche()

                elif key == ord('d'):
                    robot.tourner_droite()

                elif key == ord(' ') or key == ord('x'):
                    robot.arreter()
                    if key == ord('x'):
                        break
                robot.arreter()

            else:
                texte = f"VOIE LIBRE ({confiance * 100:.1f}%)"
                couleur = (0, 255, 0)
                cv2.putText(frame, texte, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, couleur, 2)

            cv2.imshow(window_name, frame)


    finally:
        robot.arreter()
        camera.release()
        cv2.destroyAllWindows()
        print("\nSystème arrêté.")

if __name__ == "__main__":
    main()