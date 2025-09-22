#Auteur: Marc-Antoine Faucher
#Date: 2025-09-15


import threading
from led import DEL
from gpiozero import DigitalInputDevice, DigitalOutputDevice
import time



class Sonar:
    VITESSE_DU_SON = 34300.0  # cm/s

    def __init__(self, trigger_pin, echo_pin, led_pin):
        self.trigger = DigitalOutputDevice(trigger_pin)
        self.echo = DigitalInputDevice(echo_pin)
        self.echo.when_activated = self.demarrer
        self.echo.when_deactivated = self.arreter
        self.start_time = 0
        self.distance = 0
        self.running = True
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()
        self.led = DEL(led_pin)


    def loop(self):
        while self.running:
            self.trigger.on()
            time.sleep(1)
            self.trigger.off()
            time.sleep(1)



    def ajouter_distance(self, distance):
        self.distance = distance

    def demarrer(self):
        self.start_time = time.perf_counter()

    def arreter(self):
        if self.start_time == 0:
            return
        duration = time.perf_counter() - self.start_time
        distance = duration * Sonar.vitesse_du_son / 2
        self.distance = distance
        blink_speed = self.distance / 60
        if distance < 60:
            self.led.clignoter(blink_speed, blink_speed)
        self.start_time = 0

    def get_distance(self):
        return self.distance

