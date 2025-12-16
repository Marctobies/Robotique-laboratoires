#Etienne La Rochelle
#2025-09-29

import numpy
import cv2
from picamera2 import Picamera2

class Camera:
    LARGEUR = 320
    HAUTEUR = 248
    AIRE_IMAGE = LARGEUR * HAUTEUR
    AIRE_MIN = AIRE_IMAGE / 2000 #Plus haut = voie plus loin
    AIRE_MAX = AIRE_IMAGE / 60 #plus bas = voie plus proche
    IMAGE_DIVISION = 4 #divise l'image en section qui détermines si l'objet est a gauche, centre ou droite
    TEINTE_MIN, TEINTE_MAX = [0,172,203], [10,255,255] #Balle orange

    def __init__(self):
        self.picam2 = Picamera2()
        self.config = self.picam2.create_preview_configuration(main={"format": 'RGB888', "size": (self.LARGEUR, self.HAUTEUR)})
        self.picam2.align_configuration(self.config)
        (largeur_img, hauteur_img) = self.config["main"]["size"]
        self.picam2.configure(self.config)
        self.picam2.start()
        self.teinte_min = numpy.array(self.TEINTE_MIN)
        self.teinte_max = numpy.array(self.TEINTE_MAX)
        self.x, self.y , self.l, self.h = 0, 0, 0, 0
        self.quadrant_gauche = self.LARGEUR / self.IMAGE_DIVISION
        self.quadrant_droit = (self.LARGEUR / self.IMAGE_DIVISION) * (self.IMAGE_DIVISION - 1)
            
    def capturer_image(self):
        image = self.picam2.capture_array()
        image_HSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        image_BIN = cv2.inRange(image_HSV, self.teinte_min, self.teinte_max)    
        self.creer_contours(image_BIN, image)
        return image

    def creer_contours(self, image_BIN, image):
        contours, _ = cv2.findContours(image_BIN, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            self.x, self.y, self.l, self.h = cv2.boundingRect(largest_contour)
            cv2.rectangle(image,(self.x,self.y),(self.x+self.l,self.y+self.h),(255,0,0),2)
        else:
            self.x, self.y , self.l, self.h = 0, 0, 0, 0

    def distance_suivie(self):
        aire_rect = self.l * self.h
        if aire_rect >= self.AIRE_MIN and aire_rect <= self.AIRE_MAX:
            return True
        else:
            return False

    def analyser_position(self):
        if self.l == 0:
            return "aucun"
        milieu = (self.x+self.l/2)
        position = "centre"
        if milieu < self.quadrant_gauche:
            position = "gauche"
        elif milieu > self.quadrant_droit:
            position = "droite"
        return position
    
    def ecrire_fenetre(self, text, couleur):
        img = self.capturer_image()
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        tailleFont = 1
        epaisseur = 2
        image = cv2.putText(img, text, org, font, tailleFont,
                            couleur, epaisseur, cv2.LINE_AA) 
    
    def creation_modele(self):
        while True:
            image = self.capturer_image()
            cv2.imshow("Modele", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                modele = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                modele = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                cv2.imwrite('image_modele.bmp', modele)              
     
    def arreter(self):
        self.picam2.stop()
