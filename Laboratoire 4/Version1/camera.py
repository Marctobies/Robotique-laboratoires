import cv2
from picamera2 import Picamera2, Preview
import numpy as np

class Camera:
    def __init__(self, largeur=640, hauteur=480):
        self.LARGEUR = largeur
        self.HAUTEUR = hauteur
        self.picam2 = Picamera2()
        
        self.TEINTE_MIN = np.array([0, 172, 203])
        self.TEINTE_MAX = np.array([10, 255, 255])
        
        self.SURFACE_MIN = 500    
        self.SURFACE_MAX = 50000  
        self.MARGE_CENTRE = 100   
        
        config = self.picam2.create_preview_configuration(
            main={"format": 'RGB888', "size": (self.LARGEUR, self.HAUTEUR)})
        self.picam2.align_configuration(config)
        self.picam2.configure(config)
        self.picam2.start()


    def capture(self):
     
        frame_bgr = self.picam2.capture_array()
        frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
        
        frame_disc = cv2.inRange(frame_hsv, self.TEINTE_MIN, self.TEINTE_MAX)
     
        
        contours, _ = cv2.findContours(frame_disc, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        position_balle = None
        surface_balle = 0 
        
        plus_grande_aire = 0
        meilleur_contour = None
        
        for c in contours:
            x, y, l, h = cv2.boundingRect(c)
            aire_rect = l * h
            
            if aire_rect > plus_grande_aire:
                plus_grande_aire = aire_rect
                meilleur_contour = c
        
        if meilleur_contour is not None:
            surface_balle = plus_grande_aire
            x, y, l, h = cv2.boundingRect(meilleur_contour)
            
            centre_x = x + l / 2
            centre_y = y + h / 2
            position_balle = (centre_x, centre_y)

        cv2.imshow("Image BGR", frame_bgr)
        cv2.imshow("Image Binaire", frame_disc)
        
        return position_balle, surface_balle



    def analyse(self, position_balle, surface_balle):
        if position_balle is None:
            return "ARRETER"  
        
        if surface_balle < self.SURFACE_MIN or surface_balle > self.SURFACE_MAX:
            return "ARRETER" 
        
        centre_image = self.LARGEUR / 2
        x_balle = position_balle[0]
        
        if abs(x_balle - centre_image) < self.MARGE_CENTRE:
            return "AVANCER"
        elif x_balle < centre_image:
            return "GAUCHE"
        else:
            return "DROITE"
    
    



    def release(self):
        cv2.destroyAllWindows()



