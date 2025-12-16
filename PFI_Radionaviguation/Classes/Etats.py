#Etienne La Rochelle
#2025-11-17

from enum import Enum

class Etats(Enum):
    ARRET = 0
    AVANCE = 1
    RECULE = 2
    ROTATION_GAUCHE = 3
    ROTATION_DROITE = 4
    OBSTACLE_DETECTE = 5