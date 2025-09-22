#Auteur: Marc-Antoine Faucher
#Date: 2025-09-15


from led import DEL
from gpiozero import DigitalInputDevice, DigitalOutputDevice
import time

class Sonar:
    VITESSE_DU_SON = 34300.0  # cm/s
    FENETRE = 5
    valeurs_passees = []

    def __init__(self, trigger_pin, echo_pin, led_pin):
        self.trigger = DigitalOutputDevice(trigger_pin)
        self.echo = DigitalInputDevice(echo_pin)
        self.echo.when_activated = self.demarrer
        self.echo.when_deactivated = self.arreter
        self.debut_temps = 0
        self.distance = 0
        self.led = DEL(led_pin)
        self.dernier_trigger_temps = 0
        self.interval_trigger = 0.1
        self.distance_max = 100

    def mesurer_distance(self):
        temps_actuel = time.perf_counter()

        if temps_actuel - self.dernier_trigger_temps >= self.interval_trigger:
            self.trigger.on()
            time.sleep(0.00001)
            self.trigger.off()
            self.dernier_trigger_temps = temps_actuel

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
            self.valeurs_passees.pop(min(self.valeurs_passees))
            self.valeurs_passees.pop(max(self.valeurs_passees))
            self.distance = sum(self.valeurs_passees) / len(self.valeurs_passees)
        else:
            self.distance = sum(self.valeurs_passees) / len(self.valeurs_passees)

        self.distance = distance
        self.mise_a_jour_led()
        self.debut_temps = 0

    def mise_a_jour_led(self):
        if self.distance_max > self.distance > 0:
            vitesse_clignotement = max(0.05, (self.distance / self.distance_max) * 1.0)
            self.led.clignoter(vitesse_clignotement, vitesse_clignotement)
        else:
            self.led.eteindre()

    def get_distance(self):
        self.mesurer_distance()
        return self.distance

