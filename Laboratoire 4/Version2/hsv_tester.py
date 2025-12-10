# Modifié par J. S. Morales
# 21 septembre 2025


import cv2
import numpy as np



def track_bar_cb(x):
    pass

LARGEUR = 640
HAUTEUR = 480

# --- Initialisation de la caméra d'ordinateur (webcam) ---
cap = cv2.VideoCapture(0) # 0 est généralement l'ID de la webcam par défaut
if not cap.isOpened():
    raise IOError("Erreur: Impossible d'ouvrir la webcam.")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, LARGEUR)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HAUTEUR)
# ---------------------------------------------------------

titre_fenetre = "HSV Tester"
cv2.namedWindow(titre_fenetre)
cv2.createTrackbar('Teinte min',  titre_fenetre, 0, 179, track_bar_cb)
cv2.createTrackbar('Teinte max', titre_fenetre, 179, 179, track_bar_cb)
cv2.createTrackbar('Saturation min', titre_fenetre, 0,255, track_bar_cb)
cv2.createTrackbar('Saturation max', titre_fenetre, 255, 255, track_bar_cb)
cv2.createTrackbar('Valeur min', titre_fenetre, 0, 255, track_bar_cb)
cv2.createTrackbar('Valeur max', titre_fenetre, 255, 255, track_bar_cb)

print(f"Pour quitter presser la touche 'q'.")

try:
    terminer = False
    while not terminer:

        # Lire les valeurs actuelles des curseurs
        min_teinte = cv2.getTrackbarPos('Teinte min', titre_fenetre)
        max_teinte = cv2.getTrackbarPos('Teinte max', titre_fenetre)
        sat_min = cv2.getTrackbarPos('Saturation min', titre_fenetre)
        sat_max = cv2.getTrackbarPos('Saturation max', titre_fenetre)
        val_min = cv2.getTrackbarPos('Valeur min', titre_fenetre)
        val_max = cv2.getTrackbarPos('Valeur max', titre_fenetre)

        # Créer les tableaux NumPy pour les seuils min et max à partir des valeurs des curseurs
        teinte_min = np.array([min_teinte, sat_min, val_min])
        teinte_max = np.array([max_teinte, sat_max, val_max])

        # Capturer une image de la webcam
        ret, frame_bgr = cap.read()
        if not ret:
            print("Erreur de capture d'image. Fin du programme.")
            break
        
        frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
        frame_disc = cv2.inRange(frame_hsv, teinte_min, teinte_max)
        cv2.imshow("Image BGR", frame_bgr)
        cv2.imshow("Image disc (Masque)", frame_disc)
        choix = cv2.waitKey(30)
        if  choix == ord('q'):
            terminer = True

finally:
    # S'assurer de bien libérer les ressources
    cap.release()
    cv2.destroyAllWindows()
