import numpy as np
import cv2
from Moteur import Moteur

class Robot:
    def __init__(self):
        self.MoteurGauche = Moteur(6, 5, 13)
        self.MoteurDroite = Moteur(15, 14, 18)

    def avancer(self, vitesse):
        self.MoteurGauche.avancer(vitesse)
        self.MoteurDroite.avancer(vitesse)

    def reculer(self, vitesse):
        self.MoteurGauche.reculer(vitesse)
        self.MoteurDroite.reculer(vitesse)

    def arreter(self):
        self.MoteurGauche.arreter()
        self.MoteurDroite.arreter()

    def freiner(self):
        self.MoteurGauche.freiner()
        self.MoteurDroite.freiner()

    def tourner_gauche(self, vitesse1, vitesse2):
        self.MoteurGauche.avancer(vitesse1)
        self.MoteurDroite.avancer(vitesse2)

    def tourner_droite(self, vitesse1, vitesse2):
        self.MoteurGauche.avancer(vitesse1)
        self.MoteurDroite.avancer(vitesse2)

    def pivot_gauche(self, vitesse):
        self.MoteurGauche.reculer(vitesse)
        self.MoteurDroite.avancer(vitesse)

    def pivot_droite(self, vitesse):
        self.MoteurGauche.avancer(vitesse)
        self.MoteurDroite.reculer(vitesse)


