import cv2

class Detecteur:

    def __init__(self, lower_hsv, upper_hsv):
        self.lower_hsv = lower_hsv
        self.upper_hsv = upper_hsv



    def detect(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_hsv, self.upper_hsv)
        contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            cv2.drawContours(frame_bgr, contours, -1, (255, 0, 0), 2)
