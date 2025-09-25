from odometre import Odometre
import numpy as np
import cv2
from robot import Robot
import time

def main():
    img = np.zeros((256, 256, 3), np.uint8)
    cv2.imshow('labo2', img)

    robot = Robot()
    vitesse = 0.5
    robot.modifier_vitesse(vitesse)

    odometre = Odometre(encodeur_gauche_pin=27, encodeur_droite_pin=22)

    key = cv2.waitKeyEx(10)

    try:
        while key != ord('x'):

            distance_odometre = odometre.get_distance_parcourue()

            img = np.zeros((256, 256, 3), np.uint8)
            cv2.putText(img, f"Distance: {distance_odometre:.1f} cm", (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
            cv2.imshow('labo2', img)


            if key == ord('x'):
                robot.arreter()
                break

            elif key == ord('m'):
                odometre.avancer_distance(100.0)
                robot.avancer()
                odometre.attendre()
                robot.arreter()
                print("Le robot a avancé d'un mètre.")

    finally:
        robot.arreter()
        odometre.desactiver_encodeur()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
