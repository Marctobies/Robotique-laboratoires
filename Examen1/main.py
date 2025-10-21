#Auteur: Marc-Antoine Faucher
#Date: 2025-10-20
#Examen 1 - Conception d'environnements intelligents


import cv2
from picamera2 import Picamera2, Preview
import numpy as np
from gpiozero import DigitalOutputDevice, DigitalInputDevice, PWMOutputDevice, Event

class Camera:
    def __init__(self):
        self.picam2 = Picamera2()
        config = self.picam2.create_preview_configuration(
            main={"format": 'RGB888', "size": (640, 480)})
        self.TEINTE_MIN = np.array([0, 0, 128])
        self.TEINTE_MAX = np.array([255, 255, 255])
        self.picam2.align_configuration(config)
        self.picam2.configure(config)
        self.picam2.start()

    def capturer_image(self):
        frame_bgr = self.picam2.capture_array()
        frame_bin = cv2.inRange(frame_bgr, self.TEINTE_MIN, self.TEINTE_MAX)
        contours, _ = cv2.findContours(frame_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours_filtres = []
        for c in contours:
            aire = cv2.contourArea(c)
            if aire > 10000:
                contours_filtres.append(c)
        return len(contours_filtres)
    
class Moteur:
    def __init__(self, pin_avancer, pin_reculer, pin_puissance):
        self.avancer_pin = DigitalOutputDevice(pin_avancer)
        self.reculer_pin = DigitalOutputDevice(pin_reculer)
        self.vitesse = PWMOutputDevice(pin_puissance)

    def avancer(self, vitesse):
        if self.valider_vitesse(vitesse):
            self.reculer_pin.off()
            self.avancer_pin.on()
            self.vitesse.value = vitesse

class Odometre:
    def __init__(self, encodeur_gauche_pin, encodeur_droite_pin):
        self.encodeur_gauche = DigitalInputDevice(encodeur_gauche_pin, pull_up=True)
        self.encodeur_droite = DigitalInputDevice(encodeur_droite_pin, pull_up=True)
        self.event = Event()
        self.transitions_droite = 0
        self.encodeur_droite.when_activated = self.callback_encodeur_droite
        self.encodeur_droite.when_deactivated = self.callback_encodeur_droite

    def callback_encodeur_droite(self):
        self.transitions_droite += 1
        if self.transitions_droite >= 10:
            self.event.set()
            self.transitions_droite = 0
            self.encodeur_droite.when_activated = None
            

class Robot:
    def __init__(self):
        self.MoteurGauche = Moteur(6, 5, 13)
        self.MoteurDroite = Moteur(15, 14, 18)
    def avancer(self, vitesse):
        self.MoteurGauche.avancer(vitesse)
        self.MoteurDroite.avancer(vitesse)


def main():
    robot = Robot()
    camera = Camera()
    odometre = Odometre(23, 24)
    nombre_images_traitees = 0
    vitesse_avancee = 0.5
    robot.avancer(vitesse_avancee)
    while nombre_images_traitees < 10:
        odometre.event.wait()
        nombre_contours = camera.capturer_image()
        print(f"Nombre de contours avec aire > 10 000 pixels: {nombre_contours}")
        nombre_images_traitees += 1
        odometre.event.clear()
        odometre.encodeur_droite.when_activated = odometre.callback_encodeur_droite
    robot.MoteurGauche.arreter()
    robot.MoteurDroite.arreter()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()