# Laboratoires de Robotique - Conception d'environnements intelligents

Ce dossier contient l'ensemble des travaux pratiques et laboratoires réalisés dans le cadre du cours de Conception d'environnements intelligents. L'objectif de ces laboratoires est de développer progressivement les capacités d'un robot mobile (basé sur Raspberry Pi) en intégrant divers capteurs, de la vision par ordinateur et de l'intelligence artificielle.
👥 Auteurs

    Marc-Antoine Faucher

    Loik Boulanger

    Collaborations mentionnées : Étienne (Lab 8)

📂 Contenu des Laboratoires

Chaque sous-dossier représente une étape clé dans le développement des fonctionnalités du robot.

**Laboratoire 1 : Contrôle Manuel et Motorisation**

Objectif : Prise en main du robot et implémentation du contrôle moteur de base.

    Fonctionnalités :

        Pilotage manuel du robot via le clavier (Z/Q/S/D ou W/A/S/D).

        Gestion logicielle de la vitesse (accélération/décélération).

        Implémentation de manœuvres de base (avancer, reculer, pivots, virages).


**Laboratoire 2 : Capteurs et Actionneurs Simples**

Objectif : Intégration des premiers périphériques d'interaction.

    Fonctionnalités :

        Utilisation de LEDs pour le feedback visuel.

        Utilisation du capteur sonar pour la détection de proximité basique.


**Laboratoire 3 : Odométrie**

Objectif : Suivi de la position et du déplacement du robot.

    Fonctionnalités :

        Calcul des distances parcourues via les encodeurs des moteurs.


**Laboratoire 4 : Vision par Ordinateur (Suivi d'objet)**

Objectif : Rendre le robot capable de suivre un objet coloré (ex: une balle).

    Fonctionnalités :

        Traitement d'image avec OpenCV pour détecter des contours.

        Asservissement visuel : le robot ajuste sa direction ("GAUCHE", "DROITE", "AVANCER") en fonction de la position de la balle dans l'image.


**Laboratoire 5 : Traitement d'Images Avancé**

Objectif : Manipulation d'images et reconnaissance de formes.

    Contenu : Utilisation de masques et de modèles de référence (fichiers masque.png, modele.png).

**Laboratoire 6 : Navigation et LiDAR**

Objectif : Navigation autonome avec évitement d'obstacles et orientation précise.

    Fonctionnalités :

        Intégration d'un LiDAR (YDLidar) pour scanner l'environnement à 360°.

        Détection d'obstacles et arrêt d'urgence autonome.

        Navigation programmée (ex: parcours carré) utilisant un capteur d'orientation (IMU) pour des virages précis à 90°.


**Laboratoire 7 : Intelligence Artificielle (Détection d'Obstacles)**

Objectif : Classification d'images en temps réel pour la navigation.

    Fonctionnalités :

        Utilisation d'un modèle de Deep Learning (modele_obstacle.pt) entraîné pour reconnaître les obstacles.

        Classification en temps réel du flux vidéo (Classe "Obstacle" vs "Libre").

        Affichage du niveau de confiance (%) et arrêt automatique du robot si un obstacle est identifié par l'IA.

        Collecte de données (collecte_image.py) pour constituer le dataset d'entraînement.


**Laboratoire 8 & PFI : Intégration Finale**

Objectif : Projet final intégrant l'ensemble des technologies.

    Fonctionnalités :

        Communication radio pour le contrôle ou la télémétrie.

        Manipulation d'objets (gestion d'une pince).

        Combinaison de la navigation LiDAR, de la vision et des capteurs.

