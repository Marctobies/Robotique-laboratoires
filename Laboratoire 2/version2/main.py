#Auteur: Marc-Antoine Faucher et Loik Boulanger
#Date: 2025-09-18


import numpy as np
import cv2
from robot import Robot
from sonar import Sonar

def main():
    img = np.zeros((256, 256, 3), np.uint8)
    cv2.imshow('labo2', img)

    robot = Robot()
    vitesse = 0.5
    virage = 0.2
    robot.modifier_vitesse(vitesse)

    sonar_gauche = Sonar(8, 25, 10)
    sonar_droite = Sonar(21, 20, 9)
    sonar_gauche.demarrer()
    sonar_droite.demarrer()

    try:
        while True:
            distance_gauche = sonar_gauche.get_distance()
            distance_droite = sonar_droite.get_distance()

            print(f"Dist G: {distance_gauche:.2f} cm  |  Dist D: {distance_droite:.2f} cm")


            #https://www.geeksforgeeks.org/python/python-opencv-cv2-puttext-method/
            #https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html
            img = np.zeros((256, 256, 3), np.uint8)
            cv2.putText(img, f"Gauche: {distance_gauche:.1f} cm", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(img, f"Droite: {distance_droite:.1f} cm", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            cv2.imshow('labo2', img)

            key = cv2.waitKeyEx(30)

            if key == ord('x'):
                robot.arreter()
                break

            elif key == ord('w'):
                robot.avancer()
            elif key == ord('s'):
                robot.reculer()
            elif key == ord('a'):
                robot.tourner_gauche()
            elif key == ord('d'):
                robot.tourner_droite()

            elif key == ord(' '):
                robot.freiner()

            elif key == ord('.'):
                vitesse = vitesse + 0.1
                if vitesse > 1:
                    vitesse = 1
                robot.modifier_vitesse(vitesse)

            elif key == ord(','):
                vitesse = vitesse - 0.1
                if vitesse < 0:
                    vitesse = 0
                robot.modifier_vitesse(vitesse)

            elif key == ord('q'):
                robot.moteur_gauche.avancer(vitesse * virage)
                robot.moteur_droit.avancer(vitesse)

            elif key == ord('e'):
                robot.moteur_gauche.avancer(vitesse)
                robot.moteur_droit.avancer(vitesse * virage)

    finally:
        robot.arreter()
        sonar_gauche.arreter()
        sonar_droite.arreter()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
