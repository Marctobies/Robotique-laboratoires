# Auteur: Marc-Antoine Faucher et Loik Boulanger
# Date: 2025-09-22

from gpiozero import DigitalInputDevice
import threading

class Odometre:
    # Distance en centimètres parcourue par transition d'encodeur
    # Cette valeur devra être ajustée selon votre robot et vos encodeurs
    DISTANCE_PAR_TRANSITION = 0.1  # À ajuster selon votre configuration

    def __init__(self, encodeur_gauche_pin, encodeur_droite_pin):
        """
        Constructeur de l'odométre

        Args:
            encodeur_gauche_pin (int): Numéro de la broche Out de l'encodeur gauche
            encodeur_droite_pin (int): Numéro de la broche Out de l'encodeur droit
        """
        # Création des objets DigitalInputDevice pour les encodeurs
        self.encodeur_gauche = DigitalInputDevice(encodeur_gauche_pin)
        self.encodeur_droite = DigitalInputDevice(encodeur_droite_pin)

        # Création de l'événement pour synchroniser l'attente
        self.event = threading.Event()

        # Variables pour compter les transitions
        self.transitions_gauche = 0
        self.transitions_droite = 0
        self.distance_cible = 0
        self.distance_parcourue = 0

    def _callback_encodeur_gauche_activation(self):
        """Callback appelé lors de l'activation de l'encodeur gauche"""
        self.transitions_gauche += 1
        self._calculer_distance()

    def _callback_encodeur_gauche_desactivation(self):
        """Callback appelé lors de la désactivation de l'encodeur gauche"""
        self.transitions_gauche += 1
        self._calculer_distance()

    def _callback_encodeur_droite_activation(self):
        """Callback appelé lors de l'activation de l'encodeur droit"""
        self.transitions_droite += 1
        self._calculer_distance()

    def _callback_encodeur_droite_desactivation(self):
        """Callback appelé lors de la désactivation de l'encodeur droit"""
        self.transitions_droite += 1
        self._calculer_distance()

    def _calculer_distance(self):
        """
        Calcule la distance parcourue basée sur la moyenne des transitions
        des deux encodeurs et vérifie si la distance cible est atteinte
        """
        # Calcul de la moyenne des transitions des deux encodeurs
        moyenne_transitions = (self.transitions_gauche + self.transitions_droite) / 2

        # Calcul de la distance parcourue
        self.distance_parcourue = moyenne_transitions * self.DISTANCE_PAR_TRANSITION

        # Vérification si la distance cible est atteinte
        if self.distance_parcourue >= self.distance_cible:
            self.event.set()  # Déclencher l'événement

    def avancer_distance(self, distance_cm):
        """
        Configure l'odométre pour mesurer une distance spécifique

        Args:
            distance_cm (float): Distance en centimètres à parcourir
        """
        # Réinitialiser les compteurs et l'événement
        self.transitions_gauche = 0
        self.transitions_droite = 0
        self.distance_cible = distance_cm
        self.distance_parcourue = 0
        self.event.clear()

        # Installation des callbacks pour les changements d'état des encodeurs
        self.encodeur_gauche.when_activated = self._callback_encodeur_gauche_activation
        self.encodeur_gauche.when_deactivated = self._callback_encodeur_gauche_desactivation
        self.encodeur_droite.when_activated = self._callback_encodeur_droite_activation
        self.encodeur_droite.when_deactivated = self._callback_encodeur_droite_desactivation

    def attendre(self):
        """
        Attend que la distance cible soit atteinte, puis désactive tous les callbacks
        """
        # Attendre que l'événement soit déclenché
        self.event.wait()

        # Désactiver toutes les fonctions de rappel
        self.encodeur_gauche.when_activated = None
        self.encodeur_gauche.when_deactivated = None
        self.encodeur_droite.when_activated = None
        self.encodeur_droite.when_deactivated = None

    def get_distance_parcourue(self):
        """
        Retourne la distance actuellement parcourue

        Returns:
            float: Distance parcourue en centimètres
        """
        return self.distance_parcourue

    def get_transitions_gauche(self):
        """
        Retourne le nombre de transitions détectées sur l'encodeur gauche

        Returns:
            int: Nombre de transitions
        """
        return self.transitions_gauche

    def get_transitions_droite(self):
        """
        Retourne le nombre de transitions détectées sur l'encodeur droit

        Returns:
            int: Nombre de transitions
        """
        return self.transitions_droite

    def cleanup(self):
        """
        Nettoie les ressources utilisées par l'odométre
        """
        # Désactiver tous les callbacks
        self.encodeur_gauche.when_activated = None
        self.encodeur_gauche.when_deactivated = None
        self.encodeur_droite.when_activated = None
        self.encodeur_droite.when_deactivated = None