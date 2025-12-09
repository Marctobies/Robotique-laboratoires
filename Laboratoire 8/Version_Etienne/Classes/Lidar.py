#Etienne La Rochelle et Marc-Antoine Faucher
#2025-12-01

import ydlidar
import time
import math
import cv2

class Lidar:

    PORT = "/dev/ttyUSB0"

    # Paramètres pour X4
    BAUD = 128000 
    SAMPLE_RATE = 8
    SCAN_FREQ = 7.0
    SINGLE_CHANNEL = False
    LIDAR_TYPE = ydlidar.TYPE_TRIANGLE
    PORTEE_MAX = 10.0  # en mètres



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


    def afficher_alentour(self, image):
        hauteur, largeur, _ = image.shape
        centre_x = largeur/2
        centre_y = hauteur/2

        if self.activer and self.lidar.doProcessSimple(self.scan) and len(self.scan.points) > 0:
            for point in self.scan.points:
                if point.range > self.PORTEE_MAX:
                    continue

                d = point.range
                a = point.angle
                x = -d * math.sin(a)
                y = d * math.cos(a)

                int_x = int(centre_x + (x * (largeur / 2 / self.PORTEE_MAX)))
                int_y = int(centre_y + (y * (hauteur / 2 / self.PORTEE_MAX)))
                cv2.circle(image, (int_x, int_y), radius=2, color=(0, 0, 255), thickness=-1)

        cv2.circle(image, (int(centre_x), int(centre_y)), radius=7, color=(255, 255, 255), thickness=-1)
        time.sleep(0.1)


    def tester_scan(self):
        print("Lidar test scan...")
        deja_actif = self.activer
        if not deja_actif:
            self.demarrer_scan()

        if self.lidar.doProcessSimple(self.scan) and len(self.scan.points) > 0:    
            for point in self.scan.points:
                print(point.angle, point.range)   
        time.sleep(0.1)

        if not deja_actif:
            self.arreter_scan()
        print("test lidar terminé.")


    def deconnecter_scan(self):
        if self.activer:
            self.arreter_scan()
        self.lidar.disconnecting()
        
