#Auteur: Marc-Antoine Faucher et Loik Boulanger
#Date: 2025-10-06

from camera import Camera
from robot import Robot 
import cv2


picam2 = Camera()
robot = Robot()

terminer = False


try:
    while not terminer:
        
        position_balle, surface_balle = picam2.capturer_contour()

        commande = picam2.analyse(position_balle, surface_balle)

        if commande == "AVANCER":
            robot.avancer()
        elif commande == "GAUCHE":
            robot.tourner_gauche()
        elif commande == "DROITE":
            robot.tourner_droite()
        elif commande == "ARRETER":
            robot.arreter()

        choix = cv2.waitKey(1) 
        if choix == ord('q'):
            terminer = True

finally:
    robot.arreter()
    picam2.release()
    print("Programme terminé.")