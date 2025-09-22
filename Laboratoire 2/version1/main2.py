#Auteur: Marc-Antoine Faucher
#Date: 202-09-18


import numpy as np
import cv2
from robot import Robot
from sonar2 import Sonar

def main():
    img = np.zeros((512, 512, 3), np.uint8)
    cv2.imshow('Labo 2 - Mesures de Distance', img)

    robot = Robot()

    sonar_gauche = Sonar(8, 25, 10)
    sonar_droite = Sonar(21, 20, 9)

    vitesse = 0.8
    vitesse_virage = 0.5



    while True:
        distance_gauche = sonar_gauche.get_distance()
        distance_droite = sonar_droite.get_distance()

        print(f"Distance Gauche: {distance_gauche:.2f} cm, Distance Droite: {distance_droite:.2f} cm")

        # Mettre à jour l'affichage OpenCV
        img = np.zeros((512, 512, 3), np.uint8)
        text_droite = f"Sonar Droite: {distance_droite:.2f} cm"
        text_gauche = f"Sonar Gauche: {distance_gauche:.2f} cm"
        cv2.putText(img, text_droite, (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(img, text_gauche, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow('Labo 2 - Mesures de Distance', img)


        key = cv2.waitKeyEx(100)

        if key == ord('w'):
            robot.avancer(vitesse)
            print("Avancer")

        elif key == ord('s'):
            robot.reculer(vitesse)
            print("Reculer")

        elif key == ord('a'):
            robot.pivot_gauche(vitesse)
            print("Pivot gauche")

        elif key == ord('d'):
            robot.pivot_droite(vitesse)
            print("Pivot droite")

        elif key == ord('q'):
            robot.tourner_gauche(vitesse, vitesse_virage)
            print("Tourner gauche")

        elif key == ord('e'):
            robot.tourner_droite(vitesse_virage, vitesse)
            print("Tourner droite")

        elif key == ord(' '):
            robot.freiner()
            print("Freiner")

        elif key == ord('x'):
            robot.arreter()
            print("Arrêt du robot")
            break

    # Nettoyer avant de quitter
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()