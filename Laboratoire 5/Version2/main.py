import cv2
import numpy as np

def detecter_et_compter(fichier_scene, fichier_template, seuil_confiance=0.8):
   
    print("Chargement des images...")
    img_rgb = cv2.imread(fichier_scene)
    if img_rgb is None:
        print(f"Erreur: Impossible de charger l'image de la scène : {fichier_scene}")
        return

    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    template = cv2.imread(fichier_template, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"Erreur: Impossible de charger l'image du modèle : {fichier_template}")
        return

    w, h = template.shape[::-1]
    print(f"Recherche d'un modèle de taille {w}x{h} pixels...")

    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

    locations = np.where(res >= seuil_confiance)
    
    points = list(zip(*locations[::-1]))
    
    if not points:
        print("Aucun objet détecté avec le seuil actuel.")
        return

    print(f"Détection brute : {len(points)} points trouvés au-dessus du seuil.")

    rectangles = []
    for pt in points:
        rect = [int(pt[0]), int(pt[1]), int(w), int(h)]
        found_close = False
        for r in rectangles:
            dist_x = (r[0] + r[2]/2) - (rect[0] + rect[2]/2)
            dist_y = (r[1] + r[3]/2) - (rect[1] + rect[3]/2)
            if abs(dist_x) < w/2 and abs(dist_y) < h/2:
                found_close = True
                break
        
        if not found_close:
            rectangles.append(rect)

    nombre_objets = len(rectangles)
    print(f"Détection finale : {nombre_objets} objet(s) trouvé(s) après groupement.")

    for (x, y, w, h) in rectangles:
        cv2.rectangle(img_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)

    texte_compte = f"Objets trouvés: {nombre_objets}"
    cv2.putText(img_rgb, texte_compte, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow('Objets Detectes', img_rgb)
    print("\nAppuyez sur n'importe quelle touche pour fermer la fenêtre.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    image_scene = 'modele.png'
    image_template = 'masque.png'
    
    seuil = 0.8
    
    detecter_et_compter(image_scene, image_template, seuil)