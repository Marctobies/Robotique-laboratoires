#Etienne La Rochelle et Marc-Antoine Faucher
#2025-12-11

import serial
import time

class Radionavigation:
    def __init__(self, port='/dev/ttyACM0'):
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = 115200
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 0.1
        self.ser.open()

        # Initialisation du shell
        self.ser.write(b'\r\r')
        time.sleep(1)
        self.ser.write(b'lep\n')
        self.ser.flushInput()
        self.actif = True

    def obtenir_position(self):
        self.ser.flushInput()
        pos = None
        while pos is None:
            line = self.ser.readline()              
            data = line.decode('utf-8', errors='ignore').strip()
            if data.startswith("POS"):
                parties = data.split(',')
                if len(parties) >= 3:
                    x = float(parties[1])
                    y = float(parties[2])
                    pos = (x, y)
            else:
                pos = None
        return pos

    def fermer(self):
        self.ser.close()