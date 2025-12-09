#Etienne La Rochelle et Marc-Antoine Faucher
#2025-12-01

from gpiozero import DigitalOutputDevice, PWMOutputDevice
from Classes.Moteur import Moteur
from Classes.Sonar import Sonar
from Classes.Odometre import Odometre
from Classes.Camera import Camera
from Classes.Orientation import Orientation
from Classes.IA import IA
from Classes.Lidar import Lidar
from Classes.Etats import Etats
from time import sleep
import cv2
import threading
import time

class Robot:

    def __init__(self, vitesse=0.3, 
                IN1=5, IN2=6, ENA=13, IN3=15, IN4=14, ENB=18, 
                declencheur_droit=21, echo_droit=20, led_droit=9,
                declencheur_gauche=8, echo_gauche=25, led_gauche=10,
                odometre_droit=22, odometre_gauche=27,
                ):
        self.vitesse = vitesse
        self.moteur_droit = Moteur(IN1, IN2, ENA)
        self.moteur_gauche = Moteur(IN3, IN4, ENB)
        self.sonar_droit = Sonar(declencheur=declencheur_droit, echo=echo_droit, led=led_droit)
        self.sonar_gauche = Sonar(declencheur=declencheur_gauche, echo=echo_gauche, led=led_gauche)
        self.odometre = Odometre(out_gauche=odometre_gauche, out_droit=odometre_droit)
        self.camera = Camera()
        self.orientation = Orientation()
        self.intelligence_artificielle = IA()
        self.intelligence_artificielle.charger_modele()
        self.lidar = Lidar()
        self.lidar.demarrer_scan()
        self.etat = Etats.ARRET
        self.obstacle = 0



    #--------------------#
    #-------ETATS--------#
    #--------------------#
    def changer_etat(self, nouvel_etat):
        self.etat = nouvel_etat
        if nouvel_etat == Etats.ROTATION_GAUCHE or nouvel_etat == Etats.ROTATION_DROITE:
            self.orientation.en_rotation = True
        else:
            self.orientation.en_rotation = False



    #--------------------#
    #-----MOUVEMENTS-----#
    #--------------------#
    def avancer(self, duree=0.01):
        self.changer_etat(Etats.AVANCE)
        self.moteur_gauche.avancer(self.vitesse)
        self.moteur_droit.avancer(self.vitesse)
        sleep(duree)

    def reculer(self, duree=0.01):
        self.changer_etat(Etats.RECULE)
        self.moteur_droit.reculer(self.vitesse)
        self.moteur_gauche.reculer(self.vitesse)
        sleep(duree)

    def freiner(self):
        self.changer_etat(Etats.ARRET)
        self.moteur_droit.freiner()
        self.moteur_gauche.freiner()

    def gauche(self, duree=0.01):
        self.changer_etat(Etats.ROTATION_GAUCHE)
        self.moteur_droit.reculer(self.vitesse)
        self.moteur_gauche.avancer(self.vitesse)
        sleep(duree)

    def droite(self, duree=0.01):
        self.changer_etat(Etats.ROTATION_DROITE)
        self.moteur_droit.avancer(self.vitesse)
        self.moteur_gauche.reculer(self.vitesse)
        sleep(duree)
    
    def avancer_gauche(self, duree=0.01):
        self.changer_etat(Etats.ROTATION_GAUCHE)
        self.moteur_droit.freiner()
        self.moteur_gauche.avancer(self.vitesse)
        sleep(duree)

    def avancer_droite(self, duree=0.01):
        self.changer_etat(Etats.ROTATION_DROITE)
        self.moteur_droit.avancer(self.vitesse)
        self.moteur_gauche.freiner()
        sleep(duree)

    def avancer_distance(self, distance):
        self.odometre.avancer_distance(distance)
        self.avancer()
        self.odometre.attendre()
        self.freiner()
        return self.odometre.avoir_distance()
        


    #---------------------#
    #-------VITESSE-------#
    #---------------------#
    def modifier_vitesse(self, vitesse):
        if 0 <= vitesse <= 1:
            self.moteur_droit.modifier_vitesse(vitesse)
            self.moteur_gauche.modifier_vitesse(vitesse)
            self.vitesse = vitesse
        else:
            self.vitesse = 1
            print("La vitesse doit Ãªtre comprise entre 0 et 1.")


    #---------------------#
    #------CONTROLES------#
    #---------------------#
    def control_manuel(self, touche):
        #self.detecter_obstacle()
        if touche == ord('w'): #and not self.obstacle:
            self.avancer()
        elif touche == ord('q'):
            self.avancer_gauche()
        elif touche == ord('e'):
            self.avancer_droite()
        elif touche == ord('a'):
            self.gauche()
        elif touche == ord('s'):
            self.reculer()
        elif touche == ord('d'):
            self.droite()
        elif touche == ord(' '):
            self.freiner()
        elif touche == ord(','):
            print("Diminuer vitesse")
            self.vitesse = self.vitesse*0.9
            self.modifier_vitesse(self.vitesse)
        elif touche == ord('.'):
            print("Augmenter vitesse")
            self.vitesse = self.vitesse*1.1
            self.modifier_vitesse(self.vitesse)
        elif touche == ord('x'):
            print("Arret")
            self.freiner()



    #---------------------#
    #--------SONAR--------#
    #---------------------#
    def activer_sonars(self):
        self.sonar_gauche.demarrer()
        self.sonar_droit.demarrer()
        
    def distance_sonars(self):
        return "D:" + str(self.sonar_droit.distance()) + "m   G:" + str(self.sonar_gauche.distance()) + "m"



    #----------------------#
    #--------CAMERA--------#
    #----------------------#
    def image_camera(self):
        return self.camera.capturer_image()

    def suivre_objet(self):
        position = self.camera.analyser_position()
        if position == "aucun":
            self.freiner()
        elif position == "gauche":
            self.gauche()
        elif position == "droite":
            self.droite()
        elif position == "centre" and self.camera.distance_suivie():
            self.avancer()
        else:
            self.freiner()



    #----------------------#
    #--------PYTORCH-------#
    #----------------------#
    def detecter_obstacle(self):
        self.obstacle = self.intelligence_artificielle.trouver_obstacle(self.image_camera())
        if self.obstacle == 1:
            texte_fenetre = "obstacle"
            if self.etat == Etats.AVANCE:
                self.freiner()
        


    #----------------------#
    #------ORIENTATION-----#
    #----------------------#
    def calibrer_orientation(self):
        print("Debut de la calibration.")

        liste_my = []
        liste_mz = []

        self.moteur_droit.avancer(self.vitesse)
        self.moteur_gauche.reculer(self.vitesse)

        for i in range(100):
            mx, my, mz = self.orientation.imu.read_magnetometer_data()
            liste_my.append(my)
            liste_mz.append(mz)
            time.sleep(0.1)

        self.freiner()
        self.orientation.corr_my = ( max(liste_my) + min(liste_my) ) / 2  
        self.orientation.corr_mz = ( max(liste_mz) + min(liste_mz) ) / 2

        print("Calibration terminée.")



    #----------------------#
    #---------LIDAR--------#
    #----------------------#
    def carte_alentour(self):
        if self.lidar.activer:
            image = self.image_camera()
            self.lidar.afficher_alentour(image)
            return image



    #----------------------#
    #---------ARRET--------#
    #----------------------#
    def arreter(self):
        self.moteur_droit.arreter()
        self.moteur_gauche.arreter()
        self.sonar_gauche.arreter()
        self.sonar_droit.arreter()
        self.odometre.arreter()
        self.camera.arreter()
        self.orientation.arreter()
        self.lidar.deconnecter_scan()
