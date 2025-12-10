import cv2
import numpy as np

class Camera:
    def __init__(self, largeur=640, hauteur=480):
        self.HAUTEUR = hauteur
        self.LARGEUR = largeur
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HAUTEUR)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.LARGEUR)

        # Intégration de vos mesures HSV
        # Teinte min = 0, Saturation min = 75, Valeur min = 154
        self.lower_hsv = np.array([0, 75, 154])
        # Teinte max = 37, Saturation max = 255, Valeur max = 255
        self.upper_hsv = np.array([37, 255, 255])

    def capturer_image(self):
        ret, frame = self.cap.read()
        return frame

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

    # La méthode prend maintenant l'image en paramètre pour éviter une double capture
    def detecte(self, frame_bgr):
        if frame_bgr is None:
            return None, 0, None

        frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
        frame_disc = cv2.inRange(frame_hsv, self.lower_hsv, self.upper_hsv)
        contours, _ = cv2.findContours(frame_disc, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        position_balle = None
        surface_balle = 0

        # Créer une copie de l'image pour y dessiner sans affecter l'original
        output_frame = frame_bgr.copy()

        if len(contours) > 0:
            # Trouver le plus grand contour
            c = max(contours, key=cv2.contourArea)
            surface_balle = cv2.contourArea(c)

            # On ne traite que les contours d'une taille raisonnable pour éviter le bruit
            if surface_balle > 100:
                # Calculer le rectangle englobant
                x, y, l, h = cv2.boundingRect(c)
                cv2.rectangle(output_frame, (x, y), (x + l, y + h), (0, 255, 0), 2)

                # Calculer la position du centre du rectangle
                centre_x = x + l // 2
                centre_y = y + h // 2
                position_balle = (centre_x, centre_y)

        # Retourner l'image avec les dessins, la position et la surface
        return output_frame, position_balle, surface_balle

camera = Camera(640, 480) # Utilisation d'une résolution standard
while True:
    # 1. On capture l'image une seule fois
    frame = camera.capturer_image()
    if frame is None:
        break

    # 2. On passe l'image à la méthode de détection
    frame_detecte, position, surface = camera.detecte(frame)

    # 3. On affiche l'image sur laquelle les dessins ont été faits
    cv2.imshow("Detection", frame_detecte)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()