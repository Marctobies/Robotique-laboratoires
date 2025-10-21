
# Version avec les erreurs
# def addition(a, b) # Il manque les deux points (:) après la définition de fonction
#     result = a + b
#     print("Le résultat est: " + result) # Tentative de concaténation d'un string avec un nombre
#     return result
#
# # Appel de la fonction
# addition(3, "4") # Mélange de types (int et string) sans conversion




def addition(a, b): # Ajout des deux points (:)
    result = a + b
    print("Le résultat est: " + str(result)) # Conversion de result en string avec str()
    return result

# Appel de la fonction
addition(3, 4) # Utilisation de deux entiers plutôt qu'un int et un string



# AVEC LES ERREURS
# def addition(a, b)  # Erreur: manque les deux points (:) après la définition de fonction
#     result = a + b
#     print("Le résultat est: " + result)  # Erreur: tentative de concaténation d'un string avec un nombre
#     return result
#
# # Appel de la fonction
# addition(3, "4")  # Erreur: mélange de types (int et string) sans conversion




# VERSION CORRIGÉE
# def addition(a, b):  # Correction: ajout des deux points manquants
#     result = a + b
#     print("Le résultat est: " + str(result))  # Correction: conversion du résultat en string avec str()
#     return result

# Appel de la fonction avec des types cohérents
#addition(3, 4)  # Correction: utilisation de deux entiers au lieu d'un int et d'un string


