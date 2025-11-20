# Auteur: Marc-Antoine Faucher et Loik Boulanger
# Date: 2025-11-06

from gpiozero import *
from icm20948 import ICM20948
import threading
import time
import math
import numpy as np


class Orientation:
  
    TAILLE_FENETRE_BIAIS = 100  
    INTERVALLE_MESURE = 0.05  

    def __init__(self):
        self.in_mouvement = False
        self.imu = ICM20948()
        self.ax, self.ay, self.az, self.gx, self.gy, self.gz = self.imu.read_accelerometer_gyro_data()
        self.mx, self.my, self.mz = self.imu.read_magnetometer_data()
        
        # État du robot
        self.en_mouvement = False
        
        # Données d'orientation
        self.angle_x_relatif = 0.0  # Orientation relative autour de l'axe x (roulis)
        self.cap_magnetique = 0.0   # Orientation par rapport au champ magnétique

    def get_orientation(self):
        self.ax, self.ay, self.az, self.gx, self.gy, self.gz = self.imu.read_accelerometer_gyro_data()
        self.mx, self.my, self.mz = self.imu.read_magnetometer_data()
        return self.ax, self.ay, self.az, self.gx, self.gy, self.gz, self.mx, self.my, self.mz
        # Variables pour le calcul du biais
        self.biais_gx = 0.0
        self._samples_gx = []

    def get_orientation_actuelle(self):
        return self.ax, self.ay, self.az, self.gx, self.gy, self.gz, self.mx, self.my, self.mz
        # Variables pour le thread
        self._thread_running = True
        self._lock = threading.Lock()
        self.thread = threading.Thread(target=self._calculer_orientation)
        self.thread.start()

#
    def _calculer_orientation(self):
        dernier_temps_mesure = time.time()

        while self._thread_running:
            # Lecture des données brutes du capteur
            ax, ay, az, gx, gy, gz = self.imu.read_accelerometer_gyro_data()
            mx, my, mz = self.imu.read_magnetometer_data()

            temps_actuel = time.time()
            dt = temps_actuel - dernier_temps_mesure
            dernier_temps_mesure = temps_actuel

            with self._lock:
                if not self.en_mouvement:
                    # Robot à l'arrêt : on calcule le biais de gx
                    self._samples_gx.append(gx)
                    if len(self._samples_gx) > self.TAILLE_FENETRE_BIAIS:
                        self._samples_gx.pop(0)
                    self.biais_gx = np.mean(self._samples_gx)
                else:
                    # Robot en mouvement : on calcule l'angle relatif
                    vitesse_angulaire_x = gx - self.biais_gx
                    self.angle_x_relatif += vitesse_angulaire_x * dt

                # En tout temps : calcul du cap magnétique
                # 1. Calcul du roulis (roll) et du tangage (pitch) à partir de l'accéléromètre
                roll = math.atan2(ay, az)
                pitch = math.atan2(-ax, math.sqrt(ay * ay + az * az))

                # 2. Compensation du magnétomètre avec le roulis et le tangage
                # Note: La calibration du magnétomètre n'est pas implémentée ici.
                # Il faudrait soustraire les biais du magnétomètre (hard/soft iron) à mx, my, mz.
                mx_comp = mx * math.cos(pitch) + mz * math.sin(pitch)
                my_comp = mx * math.sin(roll) * math.sin(pitch) + my * math.cos(roll) - mz * math.sin(roll) * math.cos(pitch)

                # 3. Calcul du cap
                self.cap_magnetique = math.degrees(math.atan2(my_comp, mx_comp))
                # Ajustement pour avoir une valeur entre 0 et 360 degrés
                if self.cap_magnetique < 0:
                    self.cap_magnetique += 360

            time.sleep(self.INTERVALLE_MESURE)




    def arreter(self):
        self._thread_running = False
        self.thread.join()
        print("Thread d'orientation arrêté.")
