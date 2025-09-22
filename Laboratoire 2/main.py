#Auteur: Marc-Antoine Faucher
#Date: 2024-09-15


import numpy as np
import cv2
from robot import Robot
from sonar2 import Sonar


def main():

    img = np.zeros((512, 512, 3), np.uint8)
    cv2.imshow('Labo 2', img)

    robot = Robot()

    sonar_gauche = Sonar(8, 25, 10)
    sonar_droite = Sonar(21, 20, 9)

    vitesse = 0.8
    vitesse_virage = 0.5

    key = cv2.waitKeyEx(10)

    while key != ord('x'):

        distance_gauche = sonar_gauche.get_distance()
        distance_droite = sonar_droite.get_distance()
        print(f"Distance Gauche: {distance_gauche:.2f} cm, Distance Droite: {distance_droite:.2f} cm")

        if key == ord('w'):
            robot.avancer(vitesse)

        elif key == ord('s'):
            robot.reculer(vitesse)

        elif key == ord('a'):
            robot.pivot_gauche(vitesse)

        elif key == ord('d'):
            robot.pivot_droite(vitesse)

        elif key == ord('q'):
            robot.tourner_gauche(vitesse, vitesse_virage)

        elif key == ord('e'):
            robot.tourner_droite(vitesse_virage, vitesse)

        elif key == ord(' '):
            robot.freiner()

        elif key == ord('x'):
            robot.arreter()
            False


if __name__ == "__main__":
    main()
