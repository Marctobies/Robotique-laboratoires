import cv2
from picamera2 import Picamera2
import numpy as np

class Camera:
    def __init__(self, largeur=640, hauteur=480):
        self.LARGEUR = largeur
        self.HAUTEUR = hauteur
        self.picam2 = Picamera2()
        
        # Valeurs HSV pour la détection de la couleur (À CALIBRER)
        self.TEINTE_MIN = np.array([0, 176, 0])
        self.TEINTE_MAX = np.array([73, 255, 253])
        
        # Paramètres d'analyse
        self.SURFACE_MIN = 500    
        self.SURFACE_MAX = 50000  
        self.MARGE_CENTRE = 100   
        
        config = self.picam2.create_preview_configuration(
            main={"format": 'RGB888', "size": (self.LARGEUR, self.HAUTEUR)})
        self.picam2.align_configuration(config)
        self.picam2.configure(config)
        self.picam2.start()

# ---

    def capture(self):
        """
        Capture l'image, trouve le centre de masse (centroïde) de la zone de couleur, 
        et retourne sa position (x, y) et sa surface. 
        L'affichage des fenêtres CV reste pour le débogage, mais sans dessin de formes.
        """
        # 1. Capture BGR et conversion HSV
        frame_bgr = self.picam2.capture_array()
        frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
        
        # 2. Binarisation (Isolation de la couleur)
        frame_disc = cv2.inRange(frame_hsv, self.TEINTE_MIN, self.TEINTE_MAX)
        
        # 3. Opérations Morphologiques (Nettoyage de l'image)
        kernel = np.ones((5,5), np.uint8)
        frame_disc = cv2.morphologyEx(frame_disc, cv2.MORPH_OPEN, kernel)
        frame_disc = cv2.morphologyEx(frame_disc, cv2.MORPH_CLOSE, kernel)
        
        # 4. Calcul des Moments et du Centroïde
        M = cv2.moments(frame_disc)
        
        position_balle = None
        surface_balle = 0 
        
        if M["m00"] > 0:
            surface_balle = M["m00"]
            centre_x = int(M["m10"] / M["m00"])
            centre_y = int(M["m01"] / M["m00"])
            position_balle = (centre_x, centre_y)
            
            # ⛔ Les lignes de dessin (cv2.circle, cv2.putText) ont été supprimées ici.
        
        # Affichage des résultats (les fenêtres restent ouvertes)
        cv2.imshow("Image BGR", frame_bgr)
        cv2.imshow("Image Binaire", frame_disc)
        
        return position_balle, surface_balle

# ---

    def analyse(self, position_balle, surface_balle):
        """ 
        Détermine l'action du robot (commande) à partir des données de la balle. 
        """
        
        if position_balle is None:
            return "ARRETER"  
        
        if surface_balle < self.SURFACE_MIN or surface_balle > self.SURFACE_MAX:
            return "ARRETER" 
        
        centre_image = self.LARGEUR // 2
        x_balle = position_balle[0]
        
        if abs(x_balle - centre_image) < self.MARGE_CENTRE:
            return "AVANCER"
        elif x_balle < centre_image:
            return "GAUCHE"
        else:
            return "DROITE"

# ---

    def release(self):
        self.picam2.stop_thread()
        cv2.destroyAllWindows()