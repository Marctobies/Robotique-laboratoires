# Auteurs: Marc-Antoine Faucher et Loik Boulanger 
# Date: 2025-10-23
# Laboratoire 5 - Programme principal


from camera import Camera


if __name__ == "__main__":
    CHEMIN_MODELE = "Images/modele.png"
    CHEMIN_MASQUE = "Images/masque.png"
    
    try:
        ma_camera = Camera()
        ma_camera.charger_modele(CHEMIN_MODELE, CHEMIN_MASQUE)
        ma_camera.run()
        
    except Exception as e:
        print(f"Une erreur est survenue: {e}")