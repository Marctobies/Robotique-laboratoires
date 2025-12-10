import serial
import time

class Radio:
    def __init__(self, port='/dev/ttyACM0'):
        self.ser = serial.Serial()
        self.ser.port = port
        self.ser.baudrate = 115200
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = 0.1
        self.ser.open()


        self.ser.flushInput()
        self.actif = True

    def obtenir_position(self):

        self.ser.write(b'\r\r')
        time.sleep(1)

        self.ser.write(b'lep\n')
        data = str(self.ser.readline())
        print(data)

        if data.startswith("b'POS"):
            parties = data.split(',')
            x = float(parties[1])
            y = float(parties[2])
            return (x, y)

        return None

    def fermer(self):
        self.ser.close()