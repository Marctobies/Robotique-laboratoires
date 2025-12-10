

# Probleme 1
mesures = [102, 104, 15, 103, 101, 300, 102]

def filtrer_donnees(liste_valeurs):
    min_value = min(liste_valeurs)
    max_value = max(liste_valeurs)
    liste_filtree = []
    for i in liste_valeurs:
        if i != max_value and i != min_value:
            liste_filtree.append(i)

    return sum(liste_filtree) / len(liste_filtree), liste_filtree



moyenne, liste_filtree = filtrer_donnees(mesures)

print (moyenne)
print(liste_filtree)



# Probleme 2
#
import math

donnees_lidar = [
    (0, 100),    # Droit devant (0 deg, 100cm) -> Devrait donner x=0, y=100
    (90, 50),    # À droite (90 deg, 50cm) -> Devrait donner x=-50, y=0 (approx)
    (180, 200)   # Derrière (180 deg, 200cm) -> Devrait donner x=0, y=-200
]

def polaire_vers_cartesien(donnees):
    resultats = []
    # VOTRE CODE ICI
    # N'oubliez pas d'utiliser math.radians(), math.sin(), math.cos()
    for angle, distance in donnees:
        angle_rad = math.radians(angle)
        x = -distance * math.sin(angle_rad)
        y = distance * math.cos(angle_rad)
        resultats.append((x, y))
    return resultats

points_xy = polaire_vers_cartesien(donnees_lidar)
for pt in points_xy:
    print(f"X: {pt[0]:.2f}, Y: {pt[1]:.2f}")


# Probleme 3

import cv2
import numpy as np

# 1. Création de l'image synthétique (Fond noir)
image = np.zeros((100, 100, 3), dtype=np.uint8)

# 2. Dessiner un carré bleu (BGR: Bleu=255, Vert=0, Rouge=0)
# cv2.rectangle(image, (start_x, start_y), (end_x, end_y), color, thickness)
cv2.rectangle(image, (30, 30), (70, 70), (255, 0, 0), -1) # Carré plein de 40x40 pixels

# VOTRE MISSION :
# 3. Convertir en HSV
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 4. Définir les bornes du bleu en HSV
# (Rappel: Dans OpenCV, Teinte Bleu est environ 120.
#  Cherchez entre 110 et 130 pour la teinte)
lower_blue = np.array([120, 100, 100])
upper_blue = np.array([130, 255, 255])

# 5. Créer le masque
masque = cv2.inRange(image_hsv, lower_blue, upper_blue)

# 6. Vérification
nombre_pixels = cv2.countNonZero(masque)
print(f"Pixels détectés : {nombre_pixels}")
# Si tout va bien, cela devrait être proche de 1600 (40x40).

