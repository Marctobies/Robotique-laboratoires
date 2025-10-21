import cv2
import numpy as np

def detecter_et_compter(fichier_scene, fichier_template, seuil_confiance=0.8):
    """
    Détecte toutes les occurrences d'un objet modèle dans une image de scène.

    Args:
        fichier_scene (str): Le chemin vers l'image principale.
        fichier_template (str): Le chemin vers l'image du modèle à rechercher.
        seuil_confiance (float): Le seuil de similarité (entre 0.0 et 1.0) pour considérer une détection comme valide.
    """
    print("Chargement des images...")
    # Charger l'image de la scène en couleur et une version en tons de gris
    img_rgb = cv2.imread(fichier_scene)
    if img_rgb is None:
        print(f"Erreur: Impossible de charger l'image de la scène : {fichier_scene}")
        return

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    # Charger l'image du modèle (template) en tons de gris
    template = cv2.imread(fichier_template, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"Erreur: Impossible de charger l'image du modèle : {fichier_template}")
        return

    # Obtenir les dimensions du modèle
    w, h = template.shape[::-1]
    print(f"Recherche d'un modèle de taille {w}x{h} pixels...")

    # Utiliser la méthode de template matching
    # TM_CCOEFF_NORMED donne un score entre -1.0 et 1.0, où 1.0 est une correspondance parfaite
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    # Trouver toutes les zones où la correspondance est supérieure à notre seuil de confiance
    locations = np.where(res >= seuil_confiance)
    
    # Inverser les coordonnées pour obtenir (x, y) et les regrouper dans une liste
    points = list(zip(*locations[::-1]))
    
    if not points:
        print("Aucun objet détecté avec le seuil actuel.")
        return

    print(f"Détection brute : {len(points)} points trouvés au-dessus du seuil.")

    # --- Grouper les rectangles qui se chevauchent ---
    # Cette étape est importante pour éviter de dessiner des dizaines de boîtes pour un seul objet
    rectangles = []
    for pt in points:
        rect = [int(pt[0]), int(pt[1]), int(w), int(h)]
        # Vérifie si le rectangle est trop proche d'un autre déjà trouvé
        found_close = False
        for r in rectangles:
            # Calcule la distance entre les centres des rectangles
            dist_x = (r[0] + r[2]/2) - (rect[0] + rect[2]/2)
            dist_y = (r[1] + r[3]/2) - (rect[1] + rect[3]/2)
            if abs(dist_x) < w/2 and abs(dist_y) < h/2:
                found_close = True
                break
        
        if not found_close:
            rectangles.append(rect)

    nombre_objets = len(rectangles)
    print(f"Détection finale : {nombre_objets} objet(s) trouvé(s) après groupement.")

    # Dessiner un rectangle vert autour de chaque objet détecté
    for (x, y, w, h) in rectangles:
        cv2.rectangle(img_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Afficher le compte sur l'image
    texte_compte = f"Objets trouvés: {nombre_objets}"
    cv2.putText(img_rgb, texte_compte, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Afficher le résultat
    cv2.imshow('Objets Detectes', img_rgb)
    print("\nAppuyez sur n'importe quelle touche pour fermer la fenêtre.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # --- MODIFIEZ CES VALEURS ---
    image_scene = 'scene.png'
    image_template = 'template.png'
    
    # Ajustez ce seuil si trop ou pas assez d'objets sont détectés.
    # Une valeur plus élevée est plus stricte.
    seuil = 0.8
    
    detecter_et_compter(image_scene, image_template, seuil)