# Auteur: Marc-Antoine Faucher et Loik Boulanger
# Date: 2025-09-22
# Modifié: 2024-04-26

from gpiozero import DigitalInputDevice
import threading

class Odometre:
    # Il faudrait revoir la façon de calculer la distance par transition
    # en prenant en compte la circonférence de la roue. Actuellement, on
    # ne prend pas en compte le fait que la circonférence de la roue pourrait changer.
    DISTANCE_PAR_TRANSITION = 0.51
    DISTANCE_DE_FREINAGE = 9

    def __init__(self, encodeur_gauche_pin, encodeur_droite_pin):
        self.encodeur_gauche = DigitalInputDevice(encodeur_gauche_pin, pull_up=True)
        self.encodeur_droite = DigitalInputDevice(encodeur_droite_pin, pull_up=True)
        self.lock = threading.Lock()

        self.event = threading.Event()

        self.transitions_gauche = 0
        self.transitions_droite = 0
        self.distance_cible = 0
        self.distance_parcourue = 0

        self.encodeur_gauche.when_activated = self.callback_encodeur_gauche
        self.encodeur_gauche.when_deactivated = self.callback_encodeur_gauche
        self.encodeur_droite.when_activated = self.callback_encodeur_droite
        self.encodeur_droite.when_deactivated = self.callback_encodeur_droite


    def callback_encodeur_gauche(self):
        with self.lock:
            self.transitions_gauche += 1
            self.calculer_distance()

    def callback_encodeur_droite(self):
        with self.lock:
            self.transitions_droite += 1
            self.calculer_distance()

    def calculer_distance(self):
        moyenne_transitions = (self.transitions_gauche + self.transitions_droite) / 2.0
        self.distance_parcourue = moyenne_transitions * self.DISTANCE_PAR_TRANSITION

        if self.distance_parcourue >= (self.distance_cible - self.DISTANCE_DE_FREINAGE):
            self.event.set()

    def avancer_distance(self, distance_cm):
        with self.lock:
            self.transitions_gauche = 0
            self.transitions_droite = 0
            self.distance_parcourue = 0
        self.distance_cible = distance_cm
        self.event.clear()

    def attendre(self):
        self.event.wait()


    def get_distance_parcourue(self):
        with self.lock:
            return self.distance_parcourue

    def desactiver_encodeur(self):
        self.encodeur_gauche.when_activated = None
        self.encodeur_gauche.when_deactivated = None
        self.encodeur_droite.when_activated = None
        self.encodeur_droite.when_deactivated = None




