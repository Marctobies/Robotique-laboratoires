from gpiozero import Servo
from time import sleep


def main(): 
    pince = Servo(17)

    while True:
        pince.min()
        sleep(2)
        pince.max()
        sleep(2)
        pince.mid()
    
if __name__ == "__main__":
    main()
    


