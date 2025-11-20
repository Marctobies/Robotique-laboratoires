# Auteurs: Marc-Antoine Faucher et Loik Boulanger 
# Date: 2025-10-23
# Laboratoire 5 - Classe Camera


import cv2
import numpy as np


class Camera:

    def __init__(self):

        self.capture_dir = "Laboratoire 5/Images"
        self.cap = cv2.VideoCapture(0)
        self.modele = None
        self.masque = None
        self.w_modele, self.h_modele = 0, 0
        
        self.SEUIL_ACCEPTATION = 0.3
        
        self.derniere_position_trouvee = None
        self.taille_roi_padding = 100 

    def charger_modele(self, chemin_modele, chemin_masque):

        self.modele = cv2.imread(chemin_modele, 0)
        self.masque = cv2.imread(chemin_masque, 0)
        self.h_modele, self.w_modele = self.modele.shape

    def rechercher_objet(self, frame):
        
        if self.modele is None:
            return frame 

        frame_resultat = frame.copy()
        frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        recherche_roi = None
        zone_de_recherche = frame_gris
        offset_recherche = (0, 0)

        if self.derniere_position_trouvee:
            x_prec, y_prec = self.derniere_position_trouvee
            
            x1 = max(0, x_prec - self.taille_roi_padding)
            y1 = max(0, y_prec - self.taille_roi_padding)
            x2 = min(frame_gris.shape[1], x_prec + self.w_modele + self.taille_roi_padding)
            y2 = min(frame_gris.shape[0], y_prec + self.h_modele + self.taille_roi_padding)
            
            zone_de_recherche = frame_gris[y1:y2, x1:x2]
            offset_recherche = (x1, y1)
            recherche_roi = (x1, y1, x2, y2)
            
            cv2.rectangle(frame_resultat, (x1, y1), (x2, y2), (255, 0, 0), 2) 

        try:
            res = cv2.matchTemplate(zone_de_recherche, self.modele, cv2.TM_CCOEFF_NORMED, mask=self.masque)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        except cv2.error:
            max_val = -1 
            self.derniere_position_trouvee = None 
        
        if max_val >= self.SEUIL_ACCEPTATION:
            haut_gauche = (max_loc[0] + offset_recherche[0], max_loc[1] + offset_recherche[1])
            bas_droite = (haut_gauche[0] + self.w_modele, haut_gauche[1] + self.h_modele)
            
            cv2.rectangle(frame_resultat, haut_gauche, bas_droite, (0, 255, 0), 2) 
            
            self.derniere_position_trouvee = haut_gauche
        
        else:
            self.derniere_position_trouvee = None
    
            if recherche_roi is not None:
                return self.rechercher_objet(frame) 

        return frame_resultat

    def run(self):
        
        while True:
            ret, frame = self.cap.read() 
            
            frame_detectee = self.rechercher_objet(frame)
            
            cv2.imshow('Laboratoire 5', frame_detectee)

            key = cv2.waitKey(1)

            if key == ord('q'):
                print("Touche 'q' pressée. Arrêt du programme.")
                break
        self.release()

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()