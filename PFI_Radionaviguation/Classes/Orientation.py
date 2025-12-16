#Etienne La Rochelle et Marc-Antoine Faucher
#2025-12-08

import threading
import time
import numpy as np
import math
from icm20948 import ICM20948


class Orientation:

    TAILLE_FENETRE_BIAIS = 10

    def __init__(self):
        self.continuer = True
        self.imu = ICM20948()
        self.en_rotation = False
        self.fil = threading.Thread(target=self.tache, args=())
        self.valeurs_gx = []
        self.biais_gx = 0.0
        self.angle_x = 0.0
        self.temps_precedent = time.perf_counter()
        self.vieux_gx = 0.0
        self.cap_magnetique = 0.0
        self.corr_my = 0.0
        self.corr_mz = 0.0

    def debuter_lecture(self):
        self.fil.start()

    def tache(self):
        # Calibration initiale
        print("Calibration du gyroscope en cours (ne pas bouger)...")
        somme_gx = 0
        count = 0
        for _ in range(40): # Env. 2 secondes
            _, _, _, gx, _, _ = self.imu.read_accelerometer_gyro_data()
            somme_gx += gx
            count += 1
            time.sleep(0.05)
        
        self.biais_gx = somme_gx / count
        print(f"Calibration terminée. Biais Gx: {self.biais_gx:.4f}")
        self.temps_precedent = time.perf_counter()

        while self.continuer:
            temps_actuel = time.perf_counter()
            delta_temps = temps_actuel - self.temps_precedent

            ax, ay, az, gx, gy, gz = self.imu.read_accelerometer_gyro_data()
            mx, my, mz = self.imu.read_magnetometer_data()

            # Intégration continue
            gx_corrige = gx - self.biais_gx
            # Trapèze pour l'intégration
            self.angle_x += delta_temps * (gx_corrige + self.vieux_gx) / 2
            self.vieux_gx = gx_corrige

            my_corrige = my - self.corr_my
            mz_corrige = mz - self.corr_mz

            self.cap_magnetique = np.degrees(np.arctan2(mz_corrige, my_corrige))
            if self.cap_magnetique < 0:
                self.cap_magnetique += 360
            self.temps_precedent = temps_actuel

            time.sleep(0.05)


    def calculer_angle_vers_point(self, position, destination): 
        dx = destination[0] - position[0]
        dy = destination[1] - position[1]

        angle_radians = math.atan2(dy, dx)

        return math.degrees(angle_radians)

    def afficher_donnees(self):
        return "X: " + str(round(self.angle_x,2)) + "Cap M: " + str(round(self.cap_magnetique))

    def obtenir_angle(self):
        return self.angle_x

    def arreter(self):
        if self.fil.is_alive():
            self.continuer = False
            self.fil.join()
