#Auteur: Marc-Antoine Faucher
#Date: 2025-09-15


from gpiozero import DigitalOutputDevice, PWMOutputDevice

class Moteur:
    def __init__(self, in1, in2, pwmpin):
        self.in1 = DigitalOutputDevice(in1)
        self.in2 = DigitalOutputDevice(in2)
        self.pwmpin = PWMOutputDevice(pwmpin)

    def avancer(self, vitesse):
        self.in1.on()
        self.in2.off()
        self.pwmpin.value = vitesse


    def reculer(self, vitesse):
        self.in1.off()
        self.in2.on()
        self.pwmpin.value = vitesse

    def arreter(self):
        self.in1.off()
        self.in2.off()
        self.pwmpin.value = 0

    def freiner(self):
        self.in1.on()
        self.in2.on()
        self.pwmpin.value = 1