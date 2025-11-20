# Auteur: Marc-Antoine Faucher et Loik Boulanger
# Date: 2025-11-10

from orientation import Orientation

def main():
    orientation = Orientation()
    try:
        orientation.start()
        while True:
            cmd = input().strip().lower()
            if cmd == 'r':
                orientation.set_rotation()
            elif cmd == 's':
                orientation.set_immobile()
            elif cmd == 'q':
                break
    finally:
        orientation.stop()


if __name__ == "__main__":
    main()