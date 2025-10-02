from camera import Camera
import numpy as np
import cv2


picam2 = Camera()



terminer = False

while not terminer:
    picam2.capture()
    choix = cv2.waitKey(30)
    if  choix == ord('q'):
        terminer = True
picam2.release()

