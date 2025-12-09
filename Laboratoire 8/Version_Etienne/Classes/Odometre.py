#Etienne La Rochelle
#2025-09-18

from gpiozero import DigitalOutputDevice, DigitalInputDevice, LED
import time
import threading

class Odometre:

    TransitionParTour = 40
    CirconferenceRoue = 21
    DistanceParTransistion = CirconferenceRoue / TransitionParTour
    DistanceFreinage =5.5
    
    def __init__(self, out_gauche, out_droit):
        self.out_gauche = DigitalInputDevice(out_gauche)
        self.out_droit = DigitalInputDevice(out_droit)
        self.attente_evenement = None
        self.cycle_gauche = 0
        self.cycle_droit = 0
        self.distance_parcourue = 0
        self.distance = 0

    def avancer_distance(self, distance):
        self.distance = distance
        self.cycle_gauche = 0
        self.cycle_droit = 0
        self.attente_evenement = threading.Event()
        self.out_gauche.when_activated=self.debut_gauche
        self.out_droit.when_activated=self.debut_droit
        self.out_gauche.when_deactivated=self.fin_changement_gauche
        self.out_droit.when_deactivated=self.fin_changement_droit

    def debut_droit(self):
        self.cycle_droit += 1
        self.distance_atteinte()

    def debut_gauche(self):
        self.cycle_gauche += 1
        self.distance_atteinte()

    def fin_changement_droit(self):
        self.cycle_droit += 1
        self.distance_atteinte()
            
    def fin_changement_gauche(self):
        self.cycle_gauche += 1
        self.distance_atteinte()
            
    def distance_atteinte(self):
        self.distance_parcourue = (self.cycle_gauche + self.cycle_droit) / 2 * self.DistanceParTransistion
        if self.distance_parcourue + self.DistanceFreinage >= self.distance:
            self.attente_evenement.set()

    def attendre(self):
        self.attente_evenement.wait()
        self.out_gauche.when_activated=None
        self.out_droit.when_activated=None
        self.out_gauche.when_deactivated=None
        self.out_droit.when_deactivated=None

    def avoir_distance(self):
        return self.distance_parcourue
        
    def arreter(self):
        self.out_gauche.close()
        self.out_droit.close()
