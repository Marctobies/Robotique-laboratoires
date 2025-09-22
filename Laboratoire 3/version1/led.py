#Auteur: Marc-Antoine Faucher et Loik Boulanger
#Date: 2025-09-18
import time

from gpiozero import LED

class DEL:
    def __init__(self, port ):
        self.led = LED(port)

    def allumer(self):
        self.led.on()

    def eteindre(self):
        self.led.off()

    def clignoter(self, on, off):
        time.sleep(0.1)
        self.led.blink(on_time= on, off_time= off)
        time.sleep(0.1)