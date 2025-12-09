# Auteur: Marc-Antoine Faucher et Loik Boulanger
# Date: 2025-11-17

import cv2
from picamera2 import Picamera2
import os
from datetime import datetime


class Camera:
    def __init__(self, largeur=640, hauteur=480):
        self.LARGEUR = largeur
        self.HAUTEUR = hauteur
        self.picam2 = Picamera2()
        
        # Configuration de la caméra
        config = self.picam2.create_preview_configuration(
            main={"format": 'RGB888', "size": (self.LARGEUR, self.HAUTEUR)})
        self.picam2.align_configuration(config)
        self.picam2.configure(config)
        self.picam2.start()
    
    def capturer_image(self):
        frame_bgr = self.picam2.capture_array()
        return frame_bgr
    
    def sauvegarder_image(self, dossier, nom_fichier):
        frame = self.capturer_image()
        
        if not os.path.exists(dossier):
            os.makedirs(dossier)
        
        chemin_complet = os.path.join(dossier, nom_fichier)
        cv2.imwrite(chemin_complet, frame)
        return chemin_complet
    
    def afficher_image(self, frame, titre="Camera"):
        cv2.imshow(titre, frame)
    
    def release(self):
        cv2.destroyAllWindows()
        self.picam2.stop()