#Auteur: Marc-Antoine Faucher et Loik Boulanger
#Date: 2025-10-06

from moteur import *
from camera import Camera
from lidar import Lidar
from pince import Pince

class Robot:
    def __init__(self):
        self.moteur_gauche = Moteur(5, 6, 13)
        self.moteur_droit = Moteur(15, 14, 18)
        self.camera = Camera()
        self.lidar = Lidar()
        self.pince = Pince(17)
        self.vitesse = 0.7

    def modifier_vitesse(self, vitesse):
        if 0 <= vitesse <= 1:
            self.vitesse = vitesse
            if self.moteur_gauche.avancer_pin.value == 1:
                self.moteur_gauche.reculer(vitesse)
            elif self.moteur_gauche.reculer_pin.value == 1:
                self.moteur_gauche.avancer(vitesse)
            if self.moteur_droit.avancer_pin.value == 1:
                self.moteur_droit.reculer(vitesse)
            elif self.moteur_droit.reculer_pin.value == 1:
                self.moteur_droit.avancer(vitesse)
        else:
            print("Vitesse invalide. Doit être entre 0 et 1.")

    def demarrer (self):
        self.lidar.demarrer_scan()
        self.camera.demarrer_camera()

    def obtenir_vue(self):
        image = self.camera.capturer_image()
        image_lidar = self.lidar.dessiner_image(image)
        return image_lidar

    def avancer(self):
        self.moteur_gauche.reculer(self.vitesse)
        self.moteur_droit.reculer(self.vitesse)

    def reculer(self):
        self.moteur_gauche.avancer(self.vitesse)
        self.moteur_droit.avancer(self.vitesse)

    def freiner(self):
        self.moteur_gauche.freiner()
        self.moteur_droit.freiner()

    def tourner_droite(self):
        self.moteur_gauche.reculer(self.vitesse)
        self.moteur_droit.avancer(self.vitesse)

    def tourner_gauche(self):
        self.moteur_gauche.avancer(self.vitesse)
        self.moteur_droit.reculer(self.vitesse)


    def tourner_gauche_leger(self):
        self.moteur_gauche.avancer(self.vitesse)
        self.moteur_droit.avancer(self.vitesse * 0.8)

    def tourner_droite_leger(self):
        self.moteur_gauche.avancer(self.vitesse * 0.8)
        self.moteur_droit.reculer(self.vitesse)

    def arreter(self):
        self.moteur_gauche.arreter()
        self.moteur_droit.arreter()
        self.lidar.arreter_scan()
        self.camera.arreter_camera()

