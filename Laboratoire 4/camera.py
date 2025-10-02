import cv2
from picamera2 import Picamera2, Preview
import numpy as np

class Camera:
    def __init__(self, largeur=640, hauteur=480):
        self.LARGEUR = largeur
        self.HAUTEUR = hauteur
        self.picam2 = Picamera2()
        self.TEINTE_MIN = [0, 176, 0]
        self.TEINTE_MAX = [73, 255, 253]
        config = self.picam2.create_preview_configuration(main={"format": 'RGB888',
                                                 "size": (self.LARGEUR, self.HAUTEUR)})
        self.picam2.align_configuration(config)
        (largeur_img, hauteur_img) = config["main"]["size"]
        self.picam2.configure(config)
        self.picam2.start()

    def capture(self):
        frame_bgr = self.picam2.capture_array()
        frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
        teinte_min = np.array(self.TEINTE_MIN)
        teinte_max = np.array(self.TEINTE_MAX)
        frame_disc = cv2.inRange(frame_hsv, teinte_min, teinte_max)
        cv2.imshow("Image BGR", frame_bgr)





    def analyse(self):



    def release(self):
        cv2.destroyAllWindows()



