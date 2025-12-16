import time
from robot import Robot

def main():
    print("Démarrage du programme de test")
    
    robot = Robot()
    
    try:
        robot.demarrer()
        print("Robot démarré. Initialisation des capteurs")
        time.sleep(2)

        print("Exécution de la routine de déplacement")
        robot.routine_déplacement()
        print("Routine de déplacement terminée.")

    except Exception as e:
        print(f"Une erreur est survenue: {e}")
    finally:
        print("Arrêt du robot")
        robot.arreter()
        robot.release()
        robot.radio.fermer()
        print("Programme terminé.")

if __name__ == "__main__":
    main()

