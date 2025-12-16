# Auteur: Marc-Antoine Faucher et Loik Boulanger
# Date: 2025-11-06

from icm20948 import ICM20948
import threading
import time
import math
import numpy as np


class Orientation:

    TAILLE_FENETRE_BIAIS = 100  
    INTERVALLE_MESURE = 0.05  
    
    def __init__(self):
        self.imu = ICM20948()
        
        self.en_mouvement = False
        
        self.angle_x_relatif = 0.0  
        self.cap_magnetique = 0.0   
        
        self.biais_gx = 0.0
        self._samples_gx = []
        
        # Attributs pour la calibration "Hard Iron" du magnétomètre
        self.corr_my = 0.0
        self.corr_mz = 0.0
        
        self._thread_running = True
        self._lock = threading.Lock()
        
        self.thread = threading.Thread(target=self._calculer_orientation)
        self.thread.daemon = True
        self.thread.start()

    def _calculer_orientation(self):
        dernier_temps_mesure = time.time()

        while self._thread_running:
            try:
                ax, ay, az, gx, gy, gz = self.imu.read_accelerometer_gyro_data()
                mx, my, mz = self.imu.read_magnetometer_data()

                temps_actuel = time.time()
                dt = temps_actuel - dernier_temps_mesure
                dernier_temps_mesure = temps_actuel

                with self._lock:
                    # 1. Calcul du biais du gyroscope (inchangé)
                    if not self.en_mouvement:
                        self._samples_gx.append(gx)
                        if len(self._samples_gx) > self.TAILLE_FENETRE_BIAIS:
                            self._samples_gx.pop(0)
                        if len(self._samples_gx) > 0:
                            self.biais_gx = np.mean(self._samples_gx)
                    
                    # 2. Calcul de l'angle relatif (inchangé)
                    else:
                        vitesse_angulaire_x = gx - self.biais_gx
                        self.angle_x_relatif += vitesse_angulaire_x * dt

                    # 3. Appliquer les corrections de calibration (Hard Iron)
                    # 
                    my_corrige = my - self.corr_my
                    mz_corrige = mz - self.corr_mz

                    # 4. Calcul du cap magnétique (corrigé selon la diapositive 18)
                    # Formule: A = arctan(mz / my) [cite: 418, 419]
                    # Utilisation de atan2(opposé, adjacent) soit atan2(mz_corrige, my_corrige) [cite: 423]
                    self.cap_magnetique = math.degrees(math.atan2(mz_corrige, my_corrige))

                    # Ajustement pour avoir une valeur entre 0 et 360 degrés
                    if self.cap_magnetique < 0:
                        self.cap_magnetique += 360

            except Exception as e:
                print(f"Erreur dans le thread d'orientation: {e}")

            time.sleep(self.INTERVALLE_MESURE)

    def get_orientation_actuelle(self):
        with self._lock:
            return self.angle_x_relatif, self.cap_magnetique, self.biais_gx

    def reinitialiser_angle_relatif(self):
        with self._lock:
            self.angle_x_relatif = 0.0
            
    def definir_calibration_magnetometre(self, corr_my, corr_mz):
        """
        Méthode appelée par le main.py après la routine de calibration
        pour stocker les offsets. [cite: 464, 465]
        """
        with self._lock:
            self.corr_my = corr_my
            self.corr_mz = corr_mz
            print(f"[Orientation] Calibration magnétomètre définie : corr_my={self.corr_my:.2f}, corr_mz={self.corr_mz:.2f}")


    def arreter(self):
        self._thread_running = False
        self.thread.join()
        print("Thread d'orientation arrêté.")