import serial 

class Radio:
    # Class attributes for default serial configuration
    DEFAULT_PORT = '/dev/ttyUSB0'
    DEFAULT_BAUDRATE = 115200
    DEFAULT_BYTESIZE = serial.EIGHTBITS
    DEFAULT_PARITY = serial.PARITY_NONE
    DEFAULT_STOPBITS = serial.STOPBITS_ONE
    DEFAULT_TIMEOUT = 1

    def __init__(self, port=DEFAULT_PORT, baudrate=DEFAULT_BAUDRATE):
        # Pass all configuration directly to the constructor.
        # This is cleaner and avoids calling open() on an already open port.
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=self.DEFAULT_BYTESIZE,
                parity=self.DEFAULT_PARITY,
                stopbits=self.DEFAULT_STOPBITS,
                timeout=self.DEFAULT_TIMEOUT
            )
        except serial.SerialException as e:
            print(f"Erreur: Impossible d'ouvrir le port série {port}. {e}")
            # Re-raise the exception or handle it as needed
            raise

        # It's common for devices to need a moment to initialize after the port is opened.
        # This write is likely to wake up the device or clear its buffer.
        self.ser.write(b'\r\r')

    def envoyer_commande(self, commande):
        # Ensure the port is open before trying to write
        if self.ser and self.ser.is_open:
            self.ser.write(commande.encode())

    def fermer(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def obtenir_donnees(self):
        if not (self.ser and self.ser.is_open):
            return ""
        # Handle potential decoding errors if the device sends invalid data
        donnees = self.ser.readline().decode('utf-8', errors='ignore').strip()
        return donnees

    # Implementing context manager for safe resource handling
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.fermer()

        self.ser.write(commande.encode())

    def fermer(self):
        self.ser.close()

    def obtenir_donnees(self):
        donnees = self.ser.readline().decode().strip()
        return donnees