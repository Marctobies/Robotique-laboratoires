# Auteur: Marc-Antoine Faucher et Loik Boulanger
# Date: 2025-10-06

import cv2
from picamera2 import Picamera2, Preview
import numpy as np


class Camera:
    def __init__(self, largeur=640, hauteur=480):
        self.LARGEUR = largeur
        self.HAUTEUR = hauteur
        self.picam2 = Picamera2()
        #Si on mettait toute les valeurs de teinte min à 0, l'image sera
        self.TEINTE_MIN = np.array([0, 172, 197])
        self.TEINTE_MAX = np.array([10, 255, 255])
        
        # Arrête le suivi si la balle est trop loin
        self.SURFACE_MIN = 500    

        # Arrête le suivi si la balle est trop proche
        self.SURFACE_MAX = 50000

        # Marge de tolérance pour considérer que la balle est au centre
        # Le robot avancera tout droit si la balle est dans cette marge
        self.MARGE_CENTRE = 200
        
        # Configuration de la caméra
        config = self.picam2.create_preview_configuration(
            main={"format": 'RGB888', "size": (self.LARGEUR, self.HAUTEUR)})
        self.picam2.align_configuration(config)
        self.picam2.configure(config)
        self.picam2.start()

    def capturer_contour(self):
       
        frame_bgr = self.picam2.capture_array()
        frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
        frame_disc = cv2.inRange(frame_hsv, self.TEINTE_MIN, self.TEINTE_MAX)
     
        contours, _ = cv2.findContours(frame_disc, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        position_balle = None
        surface_balle = 0 
        
        if len(contours) > 0:
            # Dessiner tous les contours sur frame_bgr
            cv2.drawContours(frame_bgr, contours, -1, (255, 0, 0), 2)

            # Trouver le plus grand contour
            c = max(contours, key=cv2.contourArea)

            # Calculer la surface du plus grand contour
            surface_balle = cv2.contourArea(c)
            
            # Calculer le rectangle englobant
            x, y, l, h = cv2.boundingRect(c)
            cv2.rectangle(frame_bgr, (x, y), (x + l, y + h), (0, 0, 255), 2)

            # Calculer la position du centre du rectangle
            centre_x = x + l / 2
            centre_y = y + h / 2
            position_balle = (int(centre_x), int(centre_y))

        cv2.imshow("Image BGR", frame_bgr)
        cv2.imshow("Image Binaire", frame_disc)
        
        return position_balle, surface_balle

   

    def analyse(self, position_balle, surface_balle):
        # Si la balle est trop loin ou trop proche, on arrête le robot
        if position_balle is None or surface_balle < self.SURFACE_MIN or surface_balle > self.SURFACE_MAX:
            return "ARRETER"
        
        centre_image = self.LARGEUR / 2
        x_balle = position_balle[0]
        
        # Si la balle est dans la marge du centre, on avance tout droit
        if abs(x_balle - centre_image) < self.MARGE_CENTRE:
            return "AVANCER"
        # Si la balle est à gauche du centre, on tourne à gauche
        elif x_balle < centre_image:
            return "GAUCHE"
        # Si la balle est à droite du centre, on tourne à droite
        else:
            return "DROITE"
    
    
    def release(self):
        cv2.destroyAllWindows()