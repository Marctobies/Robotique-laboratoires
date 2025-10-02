from camera import Camera
from robot import Robot 
import cv2


picam2 = Camera()
mon_robot = Robot()

terminer = False

try:
    while not terminer:
        
        position_balle, surface_balle = picam2.capture()

        commande = picam2.analyse(position_balle, surface_balle)

        if commande == "AVANCER":
            mon_robot.avancer()
        elif commande == "GAUCHE":
            mon_robot.tourner_gauche()
        elif commande == "DROITE":
            mon_robot.tourner_droite()
        elif commande == "ARRETER":
            mon_robot.arreter()

        choix = cv2.waitKey(1) 
        if choix == ord('q'):
            terminer = True

finally:
    mon_robot.arreter()
    picam2.release()
    print("Programme terminé. Moteurs et caméra désactivés.")