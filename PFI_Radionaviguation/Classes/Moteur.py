#Etienne La Rochelle
#2025-09-18

from gpiozero import DigitalOutputDevice, PWMOutputDevice
from time import sleep

class Moteur:
    def __init__(self, IN1, IN2, EN):
        self.IN1 = DigitalOutputDevice(IN1)
        self.IN2 = DigitalOutputDevice(IN2)
        self.EN = PWMOutputDevice(EN)

    def avancer(self, vitesse=1):
        self.IN1.on()
        self.IN2.off()
        self.EN.value = vitesse

    def reculer(self, vitesse=1):
        self.IN1.off()
        self.IN2.on()
        self.EN.value = vitesse
    
    def freiner(self):
        self.IN1.on()
        self.IN2.on()
        self.EN.value = 1
        
    def arreter(self):
        self.IN1.close()
        self.IN2.close()
        self.EN.close()

    def modifier_vitesse(self, vitesse):
        self.EN.value = vitesse

    def test(self):
        print("Test de la classe Moteur")

        print("--Avancer--")
        try:
            self.Avancer(0.5)
        except ValueError as e:
            print(f"Erreur: {e}")

        print("--Reculer--")
        try:
            self.Reculer(0.5)
        except ValueError as e:
            print(f"Erreur: {e}")

        print("--Freiner--")
        try:
            self.Freiner()
        except ValueError as e:
            print(f"Erreur: {e}")

        print("Test terminé")

