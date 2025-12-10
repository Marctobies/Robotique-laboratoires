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
        compteur = 0
        while compteur < 5 or activer:
            frame = robot.obtenir_vue()
            cv2.imshow(window_name, frame)
            key = cv2.waitKey(1)

            if robot.lidar.detecter_obstacle():
                print("OBSTACLE ! Arrêt d'urgence.")
                robot.reculer()
                robot.arreter()
                if key == ord('s'):
                    robot.reculer()
                elif key == ord('x'):
                    activer = False
                continue

            for i in range(4):
                robot.avancer()
                time.sleep(0.5)
                robot.arreter()
                time.sleep(0.2)

                robot.angle_x = 0.0
                robot.orientation.en_rotation = True
                robot.tourner_droite()

                while abs(robot.orientation.angle_x) < 90.0:
                    time.sleep(0.01)
                
                robot.arreter()
                print(f"Rotation {i+1} terminée. Angle mesuré: {robot.orientation.angle_x:.2f} degrés.")
                robot.orientation.en_rotation = False
                compteur += 1

            if key == ord('x'):
                robot.arreter()
                activer = False
            # if key == ord('w'):
            #     robot.avancer()

            # elif key == ord('s'):
            #     robot.reculer()

            # elif key == ord('a'):
            #     robot.tourner_gauche()

            # elif key == ord('d'):
            #     robot.tourner_droite()

            # elif key == ord(' '):
            #     robot.arreter()

            # elif key == ord('x'):
            #     activer = False
            #     robot.arreter()
    finally:
        robot.arreter()
        print("Arrêt du contrôle du robot.")

if __name__ == '__main__':
    main()
