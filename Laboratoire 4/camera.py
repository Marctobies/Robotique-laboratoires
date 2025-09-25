from picamera2 import Picamera2
import platform
import cv2

HAUTEUR = 240
LARGEUR = 320


if platform.system() == "Linux":
    picam2 = Picamera2()
    config = picam2.create_video_configuration(main={"format": 'RGB888', "size": (LARGEUR, HAUTEUR)})
    picam2.configure(config)
    picam2.start()
    terminer = False
    while not terminer:
        image = picam2.capture_array() # ou ret, image = vcap.read() sur Windows
        cv2.imshow("Test", image)
        choix = cv2.waitKeyEx(30)    # 30 ms entre chaque image => 33 FPS
        if choix ==  ord('x'):
            terminer = True

    cv2.destroyAllWindows()


image = picam2.capture_array()
