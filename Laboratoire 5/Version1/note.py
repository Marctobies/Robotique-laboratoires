import cv2
import os
from datetime import datetime


class Camera:

    def __init__(self, camera_index=0, capture_dir="Laboratoire 5/Images"):
        self.camera_index = camera_index
        self.capture_dir = capture_dir
        self.cap = cv2.VideoCapture(self.camera_index)


    def capture_image(self, frame):
        now = datetime.now()
        filename = f"capture_{now.strftime('%Y-%m-%d_%H-%M-%S')}.png"
        filepath = os.path.join(self.capture_dir, filename)

        cv2.imwrite(filepath, frame)
        print(f"Image enregistrée : {filepath}")

    def run(self):


        while True:
            ret, frame = self.cap.read()


            cv2.imshow('Caméra de feu', frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                print("Touche 'q' pressée. Arrêt du programme.")
                break
            elif key == ord(' '):
                self.capture_image(frame)

        self.release()

    def release(self):
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        print("Ressources libérées.")


if __name__ == "__main__":

        ma_camera = Camera(capture_dir="photos_classe")

        ma_camera.run()

