import numpy as np
import cv2
from Robot import Robot

# Modifier le la façon dont le robot gère la vitesse et ses déplacements
# Lorsque je recule et que je modifie la vitesse, le robot avance plutôt que de continuer avec son mouvement actuel

def main():

    img = np.zeros((512, 512, 3), np.uint8)

    cv2.imshow('Labo 1', img)

    robot = Robot()
    vitesse = 0.8
    vitesse_virage = 0.5

    while True:
        key = cv2.waitKeyEx(10)

        if key == ord('w'):
            robot.avancer(vitesse)
            print("Avancer")

        elif key == ord('s'):
            robot.reculer(vitesse)
            print("Reculer")

        elif key == ord('a'):
            robot.pivot_gauche(vitesse)

        elif key == ord('d'):
            robot.pivot_droite(vitesse)

        elif key == ord('q'):
            robot.tourner_gauche(vitesse, vitesse_virage)

        elif key == ord('e'):
            robot.tourner_droite(vitesse_virage, vitesse)

        elif key == ord('.'):
            vitesse += vitesse * 0.1
            vitesse_virage -= vitesse_virage * 0.1
            if vitesse > 1:
                vitesse = 1
            robot.avancer(vitesse)

        elif key == ord(','):
            vitesse -= vitesse * 0.1
            vitesse_virage -= vitesse_virage * 0.1
            robot.avancer(vitesse)
            if vitesse < 0.1:
                vitesse = 0.1

        elif key == ord(' '):
            robot.freiner()

        elif key == ord('x'):
            robot.arreter()
            False




if __name__ == "__main__":
    main()
