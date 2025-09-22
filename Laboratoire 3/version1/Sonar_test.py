#Auteur: Marc-Antoine Faucher
#Date: 2025-09-15

from led import DEL
from gpiozero import DigitalInputDevice, DigitalOutputDevice
import time
import threading

class Sonar:
    VITESSE_DU_SON = 34300.0  # cm/s
    FENETRE = 5

    def __init__(self, trigger_pin, echo_pin, led_pin):
        self.trigger = DigitalOutputDevice(trigger_pin)
        self.echo = DigitalInputDevice(echo_pin)
        self.echo.when_activated = self.demarrer
        self.echo.when_deactivated = self.arreter
        self.debut_temps = 0
        self.distance = 0
        self.led = DEL(led_pin)
        self.distance_max = 100
        self.valeurs_passees = []

        # Thread
        self.running = False
        self.thread = None

    def mesurer_distance(self):
        """Démarre les mesures automatiques avec thread"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._emission_continue)
            self.thread.start()

    def _emission_continue(self):
        """Thread qui émet 10 ondes par seconde"""
        while self.running:
            self.trigger.on()
            time.sleep(0.00001)
            self.trigger.off()
            time.sleep(0.1)  # 10 fois par seconde

    def arreter_mesures(self):
        """Arrête le thread proprement"""
        self.running = False
        if self.thread:
            self.thread.join()

    def demarrer(self):
        self.debut_temps = time.perf_counter()

    def arreter(self):
        if self.debut_temps == 0:
            return

        duree = time.perf_counter() - self.debut_temps
        distance = duree * Sonar.VITESSE_DU_SON / 2

        self.valeurs_passees.append(distance)

        if len(self.valeurs_passees) > self.FENETRE:
            self.valeurs_passees.pop(0)

        if len(self.valeurs_passees) >= 3:
            # Trouver et supprimer min et max
            valeur_min = min(self.valeurs_passees)
            valeur_max = max(self.valeurs_passees)

            valeurs_filtrees = self.valeurs_passees.copy()
            valeurs_filtrees.remove(valeur_min)
            valeurs_filtrees.remove(valeur_max)

            self.distance = sum(valeurs_filtrees) / len(valeurs_filtrees)
        else:
            self.distance = sum(self.valeurs_passees) / len(self.valeurs_passees)

        self.mise_a_jour_led()
        self.debut_temps = 0

    def mise_a_jour_led(self):
        if self.distance_max > self.distance > 0:
            vitesse_clignotement = max(0.05, (self.distance / self.distance_max) * 1.0)
            self.led.clignoter(vitesse_clignotement, vitesse_clignotement)
        else:
            self.led.eteindre()

    def get_distance(self):
        return self.distance

    def cleanup(self):
        self.arreter_mesures()
        self.led.eteindre()
