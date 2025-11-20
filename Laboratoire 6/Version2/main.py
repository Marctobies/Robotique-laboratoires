# Auteur: Marc-Antoine Faucher et Loik Boulanger
# Date: 2025-11-06


from robot import Robot
from orientation import Orientation  # Assurez-vous d'avoir la version corrigée
import time
import cv2
import numpy as np

def routine_calibration(robot, orientation, duree_secondes=10):
    time.sleep(3) # Laisse le temps à l'utilisateur de lire
    donnees_my = []
    donnees_mz = []
    
    # Met le robot en rotation
    robot.modifier_vitesse(0.5) # Une vitesse modérée pour la calibration
    robot.tourner_sur_place_droite() 
    
    temps_debut = time.time()
    while time.time() - temps_debut < duree_secondes:
        try:
            mx, my, mz = orientation.imu.read_magnetometer_data() 
            donnees_my.append(my)
            donnees_mz.append(mz)
        except (IOError, TimeoutError) as e:
            print(f"Erreur lecture IMU pendant calibration: {e}")
        
        time.sleep(0.05) 

    robot.arreter()
    print("Rotation terminée. Calcul des offsets...")

    if donnees_my and donnees_mz:
        max_my = max(donnees_my)
        min_my = min(donnees_my)
        max_mz = max(donnees_mz)
        min_mz = min(donnees_mz)
        
        corr_my = (max_my + min_my) / 2
        corr_mz = (max_mz + min_mz) / 2
        
        orientation.definir_calibration_magnetometre(corr_my, corr_mz)
        print(f"Offsets calculés : corr_my={corr_my:.2f}, corr_mz={corr_mz:.2f}")
    else:
        print("ERREUR: Aucune donnée magnétique collectée. Calibration échouée.")
    
    print("--- FIN CALIBRATION ---")

def main():
    
    robot = Robot()
    orientation = Orientation()

    # Laisse 1s au thread d'orientation pour s'initialiser
    time.sleep(1.0) 

    try:
        # 1. Exécuter la calibration obligatoire [cite: 19]
        routine_calibration(robot, orientation, duree_secondes=10)
        
        print("\nCalibration terminée. Début de l'affichage des données.")
        time.sleep(2)
        
        # Création d'une fenêtre pour la capture des touches avec NumPy
        img_controles = np.zeros((100, 300, 3), np.uint8)
        cv2.imshow("Controles (q ou x pour quitter)", img_controles)

        # 2. Boucle principale pour afficher les données
        while True:
            key = cv2.waitKeyEx(100) # Réduit le délai pour une meilleure réactivité
            
            if key == ord('x') or key == ord('q'):
                break
            
            en_mouvement = False
            if key == ord('w'):
                robot.avancer()
                en_mouvement = True
            elif key == ord('s'):
                robot.reculer()
                en_mouvement = True
            elif key == ord('a'):
                robot.tourner_gauche()
                en_mouvement = True
            elif key == ord('d'):
                robot.tourner_droite()
                en_mouvement = True
            elif key == ord(' '):
                robot.freiner()
            elif key == -1: # Aucune touche pressée
                robot.arreter()

            orientation.en_mouvement = en_mouvement
            angle_rel, cap, biais = orientation.get_orientation_actuelle()
            print(f"Angle X relatif: {angle_rel: 8.2f}°  |  Cap magnétique: {cap: 8.2f}°  (Biais Gx: {biais:.4f})", end="\r")

    except KeyboardInterrupt:
        print("\nArrêt demandé par l'utilisateur.")
        
    except Exception as e:
        print(f"\nUne erreur critique est survenue: {e}")
        
    finally:
        robot.arreter()
        orientation.arreter()
        cv2.destroyAllWindows()
        print("Robot arrêté et thread d'orientation terminé. Programme terminé.")

if __name__ == "__main__":
    main()