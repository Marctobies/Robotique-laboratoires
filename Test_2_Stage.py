def addition(a, b):
    try:
        nombre_a = float(a)
        nombre_b = float(b)
        result = nombre_a + nombre_b
        print("Le résultat est: " + str(result))
        return result
    except (ValueError, TypeError):
        print("Erreur: Les deux entrées doivent être des valeurs numériques")
        return None

# L'appel de la fonction
addition(3, "4")
addition("3", 4)
addition("3", "4")
addition(3, "Orange")


