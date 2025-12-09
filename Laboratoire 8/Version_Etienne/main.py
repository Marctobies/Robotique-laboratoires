#Etienne La Rochelle et Marc-Antoine Faucher
#2025-12-01

import cv2
from Classes.Robot import Robot

robot = Robot(0.7)
terminer = False

try:
    robot.lidar.tester_scan()

    while not terminer:
        image = robot.carte_alentour()
        cv2.imshow("Labo8", image)

        commande = cv2.waitKey(30)
        if commande == ord('x'):
            terminer = True
        else:
            robot.control_manuel(commande)
            
except Exception as e:
    print("Error:", e)

finally:
    robot.arreter()
    print("Releasing resources...")
    cv2.destroyAllWindows()