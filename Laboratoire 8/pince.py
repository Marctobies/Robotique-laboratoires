from gpiozero import AngularServo
from time import sleep
 

class Pince: 
    def __init__(self, pin):
        self.servo = AngularServo(pin, min_angle=-90, max_angle=90)
        self.angle_ouvert = 45
        self.angle_ferme = -45
        self.ouvrir()

    def ouvrir(self):
        self.servo.angle = self.angle_ouvert
        sleep(0.5)
        self.servo.detach()

    def fermer(self):
        self.servo.angle = self.angle_ferme
        sleep(0.5)
        self.servo.detach()
    
