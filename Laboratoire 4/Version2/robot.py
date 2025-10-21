#Auteur: Marc-Antoine Faucher et Loik Boulanger
#Date: 2025-10-06

from moteur import *

class Robot:
    def __init__(self):
        
        self.moteur_gauche = Moteur(6, 5, 13)
        self.moteur_droit = Moteur(15, 14, 18)
        self.vitesse = 0.7

    def modifier_vitesse(self, vitesse):
        if 0 <= vitesse <= 1:
            self.vitesse = vitesse
            if self.moteur_gauche.avancer_pin.value == 1:
                self.moteur_gauche.avancer(vitesse)
            elif self.moteur_gauche.reculer_pin.value == 1:
                self.moteur_gauche.reculer(vitesse)

            if self.moteur_droit.avancer_pin.value == 1:
                self.moteur_droit.avancer(vitesse)
            elif self.moteur_droit.reculer_pin.value == 1:
                self.moteur_droit.reculer(vitesse)
        else:
            print("Vitesse invalide. Doit être entre 0 et 1.")


    def avancer(self):
        self.moteur_gauche.avancer(self.vitesse)
        self.moteur_droit.avancer(self.vitesse)

    def reculer(self):
        self.moteur_gauche.reculer(self.vitesse)
        self.moteur_droit.reculer(self.vitesse)

    def freiner(self):
        self.moteur_gauche.freiner()
        self.moteur_droit.freiner()

    def tourner_droite(self):
        
        self.moteur_gauche.avancer(self.vitesse)
        self.moteur_droit.reculer(self.vitesse)

    def tourner_gauche(self):
        
        self.moteur_gauche.reculer(self.vitesse)
        self.moteur_droit.avancer(self.vitesse)

    def arreter(self):
        self.moteur_gauche.arreter()
        self.moteur_droit.arreter()

