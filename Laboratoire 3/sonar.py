#Auteur: Marc-Antoine Faucher et Loik Boulanger
#Date: 2025-09-18

import time
from gpiozero import DigitalInputDevice, DigitalOutputDevice
from led import DEL

class Sonar:
    VITESSE_DU_SON = 34300.0  # cm/s

    def __init__(self, trigger_pin: int, echo_pin: int, led_pin: int):
        self.trigger = DigitalOutputDevice(trigger_pin)
        self.echo = DigitalInputDevice(echo_pin)
        self.led = DEL(led_pin)

        self.distance = 0.0
        self.debut_temps = 0.0
        self.distance_max = 100.0
        self._running = False

        self.echo.when_activated = self._on_echo_high
        self.echo.when_deactivated = self._on_echo_low

    def demarrer(self):
        self._running = True

    def arreter(self):
        self._running = False
        self.led.eteindre()

    def _on_echo_high(self):
        self.debut_temps = time.perf_counter()

    def _on_echo_low(self):
        duree = time.perf_counter() - self.debut_temps
        self.distance = (duree * Sonar.VITESSE_DU_SON) / 2.0
        self.debut_temps = 0.0
        self.mise_a_jour_led()

    def mesurer_distance(self):
        self.trigger.off()
        time.sleep(0.000002)
        self.trigger.on()
        time.sleep(0.00001)
        self.trigger.off()

        time.sleep(0.02)

    def mise_a_jour_led(self):
        distance = self.distance
        if 0 < distance < self.distance_max:
            temps = max(0.05, (distance / self.distance_max) * 1.0)
            self.led.clignoter(temps, temps)
        else:
            self.led.eteindre()

    def get_distance(self):
        self.mesurer_distance()
        return self.distance
