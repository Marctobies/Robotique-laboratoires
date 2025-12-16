#Auteur: Marc-Antoine Faucher et Loik Boulanger
#Date: 2025-10-06

from moteur import *
from camera import Camera
from lidar import Lidar
from pince import Pince
from orientation import Orientation
from radio import Radio
import math
import time



class Robot:
    def __init__(self):
        self.moteur_gauche = Moteur(5, 6, 13)
        self.moteur_droit = Moteur(15, 14, 18)
        self.camera = Camera()
        self.lidar = Lidar()
        self.pince = Pince(17)
        self.orientation = Orientation()
        self.radio = Radio()
        self.vitesse = 0.7


    def déplacer_vers_points(self, dx, dy):
        print("Attente de la position initiale...")
        pos_depart = self.radio.obtenir_position()
        while pos_depart is None:
            time.sleep(0.5)
            pos_depart = self.radio.obtenir_position()
        
        x_actuel, y_actuel = pos_depart
        x_cible = x_actuel + dx
        y_cible = y_actuel + dy

        print(f"Déplacement de ({x_actuel}, {y_actuel}) vers cible ({x_cible}, {y_cible})")

        tolerance = 5.0
        
        while True:
            delta_x = x_cible - x_actuel
            delta_y = y_cible - y_actuel
            distance = math.sqrt(delta_x**2 + delta_y**2)

            if distance < tolerance:
                print("Destination atteinte !")
                self.arreter()
                break

            temps_avance = min(distance * 0.5, 2.0)
            self.avancer()
            time.sleep(temps_avance) 
            self.arreter()

            nouvelle_pos = self.radio.obtenir_position()
            if nouvelle_pos:
                x_actuel, y_actuel = nouvelle_pos
            else:
                print("Perte signal radio, arrêt.")
                break

    def tourner_relatif(self, angle_deg):

        self.orientation.en_rotation = True
        angle_depart = self.orientation.angle_x
        angle_objectif = angle_deg
        angle_parcouru = 0.0

        print(f"Début rotation de {angle_deg} degrés.")

        if angle_deg > 0: 
            self.tourner_gauche()
        else: 
            self.tourner_droite()

        while abs(angle_parcouru) < abs(angle_objectif):
            time.sleep(0.05)
            angle_actuel = self.orientation.angle_x
            angle_parcouru = angle_actuel - angle_depart
            print(f"Angle parcouru: {angle_parcouru:.2f}/{angle_objectif}, Actuel: {angle_actuel:.2f}")

        self.arreter()
        self.orientation.en_rotation = False
        print(f"Rotation terminée. Angle parcouru : {angle_parcouru:.2f}")


    def routine_déplacement(self):
        print("Début routine...")
        
        self.déplacer_vers_points(0, -2)
        
        time.sleep(1)

        print("Exemple: Rotation de 90 degrés à gauche...")
        self.tourner_relatif(90) 
        time.sleep(1)

        print("Exemple: Rotation de 90 degrés à droite...")
        self.tourner_relatif(-90) 
        time.sleep(1)

        print("Routine terminée.")


    def modifier_vitesse(self, vitesse):
        if 0 <= vitesse <= 1:
            self.vitesse = vitesse
            if self.moteur_gauche.avancer_pin.value == 1:
                self.moteur_gauche.reculer(vitesse)
            elif self.moteur_gauche.reculer_pin.value == 1:
                self.moteur_gauche.avancer(vitesse)
            if self.moteur_droit.avancer_pin.value == 1:
                self.moteur_droit.reculer(vitesse)
            elif self.moteur_droit.reculer_pin.value == 1:
                self.moteur_droit.avancer(vitesse)
        else:
            print("Vitesse invalide. Doit être entre 0 et 1.")

    def demarrer (self):
        self.lidar.demarrer_scan()
        self.orientation.debuter_lecture()


    def obtenir_vue(self):
        image = self.camera.capturer_image()
        image_lidar = self.lidar.dessiner_image(image)
        return image_lidar

    def avancer(self):
        self.moteur_gauche.reculer(self.vitesse)
        self.moteur_droit.reculer(self.vitesse)

    def reculer(self):
        self.moteur_gauche.avancer(self.vitesse)
        self.moteur_droit.avancer(self.vitesse)

    def freiner(self):
        self.moteur_gauche.freiner()
        self.moteur_droit.freiner()

    def tourner_droite(self):
        self.moteur_gauche.reculer(self.vitesse)
        self.moteur_droit.avancer(self.vitesse)

    def tourner_gauche(self):
        self.moteur_gauche.avancer(self.vitesse)
        self.moteur_droit.reculer(self.vitesse)


    def tourner_gauche_leger(self):
        self.moteur_gauche.avancer(self.vitesse)
        self.moteur_droit.avancer(self.vitesse * 0.8)

    def tourner_droite_leger(self):
        self.moteur_gauche.avancer(self.vitesse * 0.8)
        self.moteur_droit.reculer(self.vitesse)

    def arreter(self):
        self.moteur_gauche.arreter()
        self.moteur_droit.arreter()

    def release(self):
        self.lidar.arreter_scan()
        self.camera.release()
        self.orientation.arreter()
        
