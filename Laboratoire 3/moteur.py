#Auteur: Marc-Antoine Faucher et Loik Boulanger
#Date: 2025-09-18

from gpiozero import *


class Moteur:
    def __init__(self, pin_avancer, pin_reculer, pin_puissance):
        self.avancer_pin = DigitalOutputDevice(pin_avancer)
        self.reculer_pin = DigitalOutputDevice(pin_reculer)
        self.vitesse = PWMOutputDevice(pin_puissance)

    def valider_vitesse(self, vitesse):
        if 0 <= vitesse <= 1:
            return True
        else:
            print("Vitesse invalide. Doit être entre 0 et 1.")
            return False

    def avancer(self, vitesse):
        if self.valider_vitesse(vitesse):
            self.reculer_pin.off()
            self.avancer_pin.on()
            self.vitesse.value = vitesse

    def reculer(self, vitesse):
        if self.valider_vitesse(vitesse):
            self.avancer_pin.off()
            self.reculer_pin.on()
            self.vitesse.value = vitesse

    def freiner(self, force=1):
        self.avancer_pin.on()
        self.reculer_pin.on()
        self.vitesse.value = force

    def arreter(self):
        self.avancer_pin.off()
        self.reculer_pin.off()
        self.vitesse.value = 0
