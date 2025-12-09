import ydlidar
import math
import cv2
import numpy as np


class Lidar:
    PORT = "/dev/ttyUSB0"
    BAUD = 128000
    SAMPLE_RATE = 8
    SCAN_FREQ = 7.0
    SINGLE_CHANNEL = False
    LIDAR_TYPE = ydlidar.TYPE_TRIANGLE
    

    def __init__(self, port=PORT, modele=LIDAR_TYPE):
        self.port = port
        self.modele = modele
        ydlidar.os_init()
        self.lidar = ydlidar.CYdLidar()
        self.lidar.setlidaropt(ydlidar.LidarPropSerialPort, self.port)
        self.lidar.setlidaropt(ydlidar.LidarPropSerialBaudrate, Lidar.BAUD)
        self.lidar.setlidaropt(ydlidar.LidarPropLidarType, self.modele)
        self.lidar.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
        self.lidar.setlidaropt(ydlidar.LidarPropSampleRate, Lidar.SAMPLE_RATE)
        self.lidar.setlidaropt(ydlidar.LidarPropScanFrequency, Lidar.SCAN_FREQ)
        self.lidar.setlidaropt(ydlidar.LidarPropSingleChannel, Lidar.SINGLE_CHANNEL)
        self.lidar.initialize()
        self.scan = ydlidar.LaserScan()
        self.activer = False

    def demarrer_scan(self):
        if self.lidar.turnOn():
            self.activer = True

    def arreter_scan(self):
        if self.lidar.turnOff():
            self.activer = False

    def dessiner_image(self, image, max_distance_mm=5000):
        if not self.activer:
            return image

        r = self.lidar.doProcessSimple(self.scan)

        if not r:
            print("Erreur lors du traitement du scan.")
            return image

        hauteur, largeur, _ = image.shape
        centre_x = largeur // 2
        centre_y = hauteur // 2

        rayon_max_pixels = min(centre_x, centre_y)
        max_distance_mm_f = float(max_distance_mm)

        echelle = rayon_max_pixels / max_distance_mm_f

        cv2.circle(image, (centre_x, centre_y), 5, (0, 0, 255), -1)

        for point in self.scan.points:
            distance_m = point.range
            distance_mm = distance_m * 1000
            angle_rad = point.angle

            if distance_mm < 100 or distance_mm > max_distance_mm_f:
                continue

            distance_pixels = int(distance_mm * echelle)

            x_polar = distance_pixels * math.sin(angle_rad)
            y_polar = -distance_pixels * math.cos(angle_rad)

            point_x = int(centre_x + x_polar)
            point_y = int(centre_y + y_polar)

            if 0 <= point_x < largeur and 0 <= point_y < hauteur:
                cv2.circle(image, (point_x, point_y), 2, (0, 255, 0), -1)

        return image
