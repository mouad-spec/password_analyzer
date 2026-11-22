import pandas as pd

# =====================================================
# CONSTANTES
# =====================================================

# --- Motifs de clavier ---
LIGNES_CLAVIER = ["azertyuiop", "qsdfghjklm", "wxcvbn",
                  "qwertyuiop", "asdfghjkl", "zxcvbnm", "1234567890"]
TAILLE_MORCEAU = 4

# Tous les morceaux de 4 caractères, dans les deux sens (calculés une seule fois)
MORCEAUX_CLAVIER = set()
for ligne in LIGNES_CLAVIER:
    for sens in (ligne, ligne[::-1]):
        for i in range(len(sens) - TAILLE_MORCEAU + 1):
            MORCEAUX_CLAVIER.add(sens[i:i + TAILLE_MORCEAU])

# --- Mots de passe courants ---
MOTS_COURANTS = ["password", "motdepasse", "admin", "welcome", "bienvenue",
                 "iloveyou", "login", "secret", "football", "maroc",
                 "casablanca", "123456", "000000", "azerty", "qwerty"]

# Substitutions classiques : p@ssw0rd -> password
SUBSTITUTIONS = str.maketrans({"@": "a", "0": "o", "3": "e",
                               "$": "s", "5": "s", "4": "a", "1": "i"})

# --- Ordre figé des colonnes (à partager avec P4) ---
NOMS_FEATURES = ["longueur", "nb_minuscules", "nb_majuscules", "nb_chiffres",
                 "nb_symboles", "diversite", "nb_uniques", "ratio_uniques",
                 "max_repetition", "a_une_suite", "a_motif_clavier",
                 "a_mot_courant"]


# =====================================================
# FONCTIONS DE BASE
# =====================================================

def compter_caracteres(mdp):
    """Nombre total de caractères."""
    return len(mdp)


def compter(mdp):
    """Nombre de minuscules, majuscules, chiffres et symboles.
    Choix : l'espace compte comme symbole."""
    return {
        "minuscules": sum(c.islower() for c in mdp),
        "majuscules": sum(c.isupper() for c in mdp),
        "chiffres": sum(c.isdigit() for c in mdp),
        "symboles": sum(not c.isalnum() for c in mdp),
    }


def diversite(mdp):
    """Nombre de catégories présentes (de 0 à 4)."""
    compte = compter(mdp)
    return sum(1 for k in ("minuscules", "majuscules", "chiffres", "symboles")
               if compte[k] > 0)


def caracteres_uniques(mdp):
    """Nombre de caractères différents."""
    return len(set(mdp))


def ratio_uniques(mdp):
    """Proportion de caractères uniques (0 pour un mot de passe vide)."""
    if len(mdp) == 0:
        return 0.0
    return round(len(set(mdp)) / len(mdp), 4)


def plus_longue_repetition(mdp):
    """Longueur de la plus longue série du même caractère (ex. 'aaa' -> 3)."""
    if len(mdp) == 0:
        return 0
    maximum = 1
    actuelle = 1
    for i in range(1, len(mdp)):
        if mdp[i] == mdp[i - 1]:
            actuelle += 1
        else:
            actuelle = 1
        maximum = max(maximum, actuelle)
    return maximum


# =====================================================
# SÉQUENCES PRÉVISIBLES
# =====================================================

def _meme_type(a, b):
    """Vrai si les deux caractères sont deux lettres ou deux chiffres."""
    return (a.isalpha() and b.isalpha()) or (a.isdigit() and b.isdigit())


def suit(mdp):
    """1 si le mot de passe contient une suite de 3 caractères ou plus
    (abc, 123, cba, 321), sinon 0."""
    mot = mdp.lower()
    longueur_max = 1
    longueur_actuelle = 1
    ecart_precedent = 0

    for i in range(len(mot) - 1):
        ecart = ord(mot[i + 1]) - ord(mot[i])

        if _meme_type(mot[i], mot[i + 1]) and ecart in (1, -1):
            if ecart == ecart_precedent:
                longueur_actuelle += 1      # la série continue dans le même sens
            else:
                longueur_actuelle = 2       # nouvelle série (début ou changement de sens)
            ecart_precedent = ecart
        else:
            longueur_actuelle = 1           # paire non valide : on repart de zéro
            ecart_precedent = 0

        longueur_max = max(longueur_max, longueur_actuelle)

    return 1 if longueur_max >= 3 else 0


def motif_clavier(mdp):
    """1 si un morceau de 4 touches voisines est présent (azer, rewq...)."""
    mot = mdp.lower()
    for morceau in MORCEAUX_CLAVIER:
        if morceau in mot:
            return 1
    return 0


def mot_courant(mdp):
    """1 si un mot très courant est présent, y compris avec substitutions
    (P@ssw0rd)."""
    mot = mdp.lower()
    mot_transforme = mot.translate(SUBSTITUTIONS)
    for courant in MOTS_COURANTS:
        if courant in mot or courant in mot_transforme:
            return 1
    return 0


# =====================================================
# FONCTIONS PRINCIPALES
# =====================================================

def extraire_features(mdp):
    """Retourne un dictionnaire plat de features numériques pour UN mot de passe.
    Une entrée qui n'est pas du texte (None, NaN...) est traitée comme vide."""
    if not isinstance(mdp, str):
        mdp = ""
    cats = compter(mdp)
    return {
        "longueur": compter_caracteres(mdp),
        "nb_minuscules": cats["minuscules"],
        "nb_majuscules": cats["majuscules"],
        "nb_chiffres": cats["chiffres"],
        "nb_symboles": cats["symboles"],
        "diversite": diversite(mdp),
        "nb_uniques": caracteres_uniques(mdp),
        "ratio_uniques": ratio_uniques(mdp),
        "max_repetition": plus_longue_repetition(mdp),
        "a_une_suite": suit(mdp),
        "a_motif_clavier": motif_clavier(mdp),
        "a_mot_courant": mot_courant(mdp),
    }


def extraire_features_lot(mots_de_passe):
    """Prend une liste (ou une colonne Pandas) de mots de passe et retourne
    un DataFrame : une ligne par mot de passe, colonnes dans l'ordre de
    NOMS_FEATURES."""
    lignes = [extraire_features(mdp) for mdp in mots_de_passe]
    return pd.DataFrame(lignes, columns=NOMS_FEATURES)


# =====================================================
# ESSAIS MANUELS (ne s'exécutent pas à l'import)
# =====================================================
if __name__ == "__main__":
    print(extraire_features("Ensab123@ "))
    print(extraire_features_lot(["abc", "P@ssw0rd", "Zx9!kLm2"]))
