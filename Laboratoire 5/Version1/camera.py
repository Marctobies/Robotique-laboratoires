# Auteur: Marc-Antoine Faucher et Loik Boulanger
# Date: 2025-10-06

import cv2
from picamera2 import Picamera2, Preview
import numpy as np


class Camera:
    def __init__(self, largeur=800, hauteur=600):
        self.LARGEUR = largeur
        self.HAUTEUR = hauteur
        self.picam2 = Picamera2()
        
        self.TEINTE_MIN = np.array([0, 172, 197])
        self.TEINTE_MAX = np.array([10, 255, 255])
        
        self.SURFACE_MIN = 500

        self.SURFACE_MAX = 50000

        self.MARGE_CENTRE = 200
        
        config = self.picam2.create_preview_configuration(
            main={"format": 'RGB888', "size": (self.LARGEUR, self.HAUTEUR)})
        self.picam2.align_configuration(config)
        self.picam2.configure(config)
        self.picam2.start()

    def capturer_image(self):
        image = picam2.capture_array()