# Auteur: Marc-Antoine Faucher
# Date: 2025-12-01


import cv2
import numpy as np
import time
from camera import Camera
from lidar import Lidar
import ydlidar
from robot import Robot



def main():
    robot = Robot()
    
    activer = True
    window_name = "Fenetre"
    print("Démarrage du contrôle du robot.")
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
    robot.lidar.demarrer_scan()
    try:
        while activer:
            frame = robot.obtenir_vue()
            cv2.imshow(window_name, frame)
            key = cv2.waitKey(1)

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

            elif key == ord('x'):
                activer = False
                robot.arreter()
    finally:
        robot.arreter()
        print("Arrêt du contrôle du robot.")

if __name__ == '__main__':
    main()
