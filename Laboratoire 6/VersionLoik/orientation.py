# Auteur: Marc-Antoine Faucher et Loik Boulanger
# Date: 2025-11-10

import time
import threading
import numpy as np
from icm20948 import ICM20948
from robot import Robot

DELTA_TEMPS = 0.050
FENETRE = 20
CALIBRATION_TEMPS = 6.0
VITESSE = 0.6

class Orientation:
    def __init__(self):
        self.imu = ICM20948()

        self.robot = Robot()
        self.robot.modifier_vitesse(VITESSE)

        self.etat = "immobile"

        self.samples_gx = []
        self.biais_gx = 0.0

        self.angle_x = 0.0
        self.gx_prev = None
        self.t_prev = None

        self.corr_my = 0.0
        self.corr_mz = 0.0

        self.cap = 0.0

        self.stop_thread = False
        self.thread = threading.Thread(target=self.loop, daemon=True)

    def start(self):
        self.calibration_magnetometre()
        self.thread.start()

    def stop(self):
        self.stop_thread = True
        try:
            self.robot.arreter()
        except Exception:
            pass
        self.thread.join(timeout=2)

    def set_immobile(self):
        self.etat = "immobile"
        self.samples_gx.clear()
        self.gx_prev = None
        self.t_prev = None
        self.robot.arreter()

    def set_rotation(self):
        self.etat = "rotation"
        self.gx_prev = None
        self.t_prev = None
        self.robot.modifier_vitesse(VITESSE)
        self.robot.tourner_gauche()

    def calibration_magnetometre(self):
        my_vals, mz_vals = [], []
        t0 = time.time()

        self.robot.modifier_vitesse(VITESSE)
        self.robot.tourner_gauche()

        try:
            while time.time() - t0 < CALIBRATION_TEMPS:
                _, my, mz = self.imu.read_magnetometer_data()
                my_vals.append(my)
                mz_vals.append(mz)
                time.sleep(0.02)
        finally:
            self.robot.arreter()

        if my_vals and mz_vals:
            self.corr_my = (max(my_vals) + min(my_vals)) / 2.0
            self.corr_mz = (max(mz_vals) + min(mz_vals)) / 2.0

        print(f"Calibration: corr_my={self.corr_my:.3f}, corr_mz={self.corr_mz:.3f}")

    def loop(self):
        prochaine = time.time()
        while not self.stop_thread:
            now = time.time()

            ax, ay, az, gx, gy, gz = self.imu.read_accelerometer_gyro_data()
            mx, my, mz = self.imu.read_magnetometer_data()

            my_c = my - self.corr_my
            mz_c = mz - self.corr_mz
            angle_rad = np.arctan2(mz_c, my_c)
            self.cap = float((np.degrees(angle_rad) + 360.0) % 360.0)

            if self.etat == "immobile": b
                self.samples_gx.append(gx)
                if len(self.samples_gx) > FENETRE:
                    self.samples_gx.pop(0)
                self.biais_gx = sum(self.samples_gx) / len(self.samples_gx) if self.samples_gx else 0.0

                self.gx_prev = None
                self.t_prev = None

            else:
                gx_corr = gx - self.biais_gx
                if self.gx_prev is None:
                    self.gx_prev = gx_corr
                    self.t_prev = now
                else:
                    dt = now - self.t_prev
                    self.angle_x += dt * (gx_corr + self.gx_prev) * 0.5
                    self.angle_x = (self.angle_x + 360.0) % 360.0
                    self.gx_prev = gx_corr
                    self.t_prev = now

            print(f"Cap={self.cap:.1f}°, Angle X={self.angle_x:.1f}°  ", end='\r', flush=True)

            prochaine += DELTA_TEMPS
            reste = prochaine - time.time()
            if reste > 0:
                time.sleep(reste)
            else:
                prochaine = time.time()