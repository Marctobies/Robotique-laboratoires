import cv2
import time
from robot import Robot


def main():
    print("Démarrage du programme")
    robot = Robot()
    
    time.sleep(1)

    key = cv2.waitKey(1)
    while key != ord('q'):
        resultat = robot.navigation_radio(10, 20)
        # if resultat is not None:
        #     x, y = resultat
        #     print(f"Position du robot (X: {x:.2f}, Y: {y:.2f})")
        # else:
        #     pass

        # key = cv2.waitKey(100) 

    robot.radio.fermer()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

