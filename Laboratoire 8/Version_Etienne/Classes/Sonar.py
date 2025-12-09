#Etienne La Rochelle
#2025-09-15

from gpiozero import DigitalOutputDevice, DigitalInputDevice, LED
import time
import threading

class Sonar:

    FENETRE = 5 #nombre de valeurs a considerer pour la moyenne mobile - *doit etre plus grand que 2*
    VITESSE_SON = 343 #vitesse du son en m/s dans l'air a 20 degres celcius

    def __init__(self, declencheur, echo, led=None):
        self.verrou = threading.Lock()
        self.continuer = True
        self.debut = 1
        self.distance_recue = 0
        self.valeurs_passees = []
        self.led = None
        if led is not None: #verifie si une led est connecter au sonar
            self.led = LED(led)
        self.declencheur = DigitalOutputDevice(declencheur)
        self.declencheur_fil = threading.Thread(target=self.declencheur_function) #declenche l'ecoute du sonar
        self.echo = DigitalInputDevice(echo)
        self.echo.when_activated = self.echo_debut
        self.echo.when_deactivated = self.echo_fin
        
    def demarrer(self):
        self.declencheur_fil.start()

    def declencheur_function(self): #declenche le sonar chaque 100ms ou 10 fois par secondes
        while self.continuer:
            self.declencheur.on()
            time.sleep(0.00001)
            self.declencheur.off()
            time.sleep(0.1)

    def echo_debut(self): #retient le moment ou le sonar envoi l'onde
        self.debut = time.perf_counter()

    def echo_fin(self): #retient le moment ou le sonar recoit l'onde
        self.fin = time.perf_counter()
        distance = (self.fin - self.debut) * self.VITESSE_SON / 2
        self.valeurs_passees.append(distance)
        if len(self.valeurs_passees) >= self.FENETRE:
            del self.valeurs_passees[0]
            enlever = min(self.valeurs_passees) + max(self.valeurs_passees)
            moyenne_mobile = (sum(self.valeurs_passees)-enlever)/(len(self.valeurs_passees)-2)
            with self.verrou:
                self.distance_recue = moyenne_mobile
            if self.led != None and self.distance_recue <= 1 and self.led.value == 0:
                self.led.blink(on_time=self.distance_recue, off_time=1, n=1, background=True)

    def distance(self): #retourne la distance moyenne des dernieres mesures
        with self.verrou:
            return round(self.distance_recue,2)

    def arreter(self): #arrete le sonar
        if self.declencheur_fil.is_alive():
            self.continuer = False
            self.declencheur_fil.join()
        self.declencheur.close()
        self.echo.close()

