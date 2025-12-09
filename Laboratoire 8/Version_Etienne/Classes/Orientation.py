#Etienne La Rochelle
#2025-11-03

import threading
import time
import numpy as np
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
        while self.continuer:
            temps_actuel = time.perf_counter()
            delta_temps = temps_actuel - self.temps_precedent

            ax, ay, az, gx, gy, gz = self.imu.read_accelerometer_gyro_data()
            mx, my, mz = self.imu.read_magnetometer_data()

            if not self.en_rotation:
                self.valeurs_gx.append(gx)
                if(len(self.valeurs_gx) >= self.TAILLE_FENETRE_BIAIS):
                    del self.valeurs_gx[0]
                self.biais_gx = sum(self.valeurs_gx) / len(self.valeurs_gx)
                self.vieux_gx = 0.0
            else:
                gx_corrige = gx - self.biais_gx
                self.angle_x += delta_temps * (gx_corrige + self.vieux_gx) / 2
                self.vieux_gx = gx_corrige

            my_corrige = my - self.corr_my
            mz_corrige = mz - self.corr_mz

            self.cap_magnetique = np.degrees(np.arctan2(mz_corrige, my_corrige))
            if self.cap_magnetique < 0:
                self.cap_magnetique += 360
            self.temps_precedent = temps_actuel

            time.sleep(0.05)

    def obtenir_donnees(self):
        return "X: " + str(round(self.angle_x,2)) + "Cap M: " + str(round(self.cap_magnetique))

    def arreter(self):
        if self.fil.is_alive():
            self.continuer = False
            self.fil.join()
