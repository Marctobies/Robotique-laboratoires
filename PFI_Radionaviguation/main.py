#Etienne La Rochelle et Marc-Antoine Faucher
#2025-12-11

import cv2
from Classes.Robot import Robot

robot = Robot(0.3)
terminer = False

try:
    while not terminer:
        image = robot.image_camera()
        cv2.imshow("PFI", image)

        commande = cv2.waitKey(30)
        if commande == ord('x'):
            terminer = True
        elif commande == ord('r'):
            robot.tracer_rectangle()
            
except Exception as e:
    print("Error:", e)

finally:
    robot.arreter()
    print("Releasing resources...")
    cv2.destroyAllWindows()