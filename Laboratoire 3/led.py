#Auteur: Marc-Antoine Faucher
#Date: 2024-09-15


from gpiozero import LED

class DEL:
    def __init__(self, port ):
        self.led = LED(port)

    def allumer(self):
        self.led.on()

    def eteindre(self):
        self.led.off()

    def clignoter(self, on, off):
        self.led.blink(on_time= on, off_time= off)

