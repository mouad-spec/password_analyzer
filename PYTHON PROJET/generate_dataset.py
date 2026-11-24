"""
generate_dataset.py  -  Personne 2 (Module 2)
Génère un dataset SYNTHÉTIQUE de mots de passe fictifs et les étiquette
(Faible / Moyen / Fort) avec des règles explicites (voir regles_etiquetage.md).

Les caractéristiques sont calculées par features.py (Personne 3) : mêmes noms
de colonnes pour tout le monde.

Utilisation (depuis la racine du projet) :  python dataset/generate_dataset.py
Sortie : dataset/dataset.csv
"""
# random : pour faire des choix au hasard
import random
# string : contient des listes toutes prêtes (lettres, chiffres...)
import string
# sys : permet de modifier les chemins où Python cherche les modules
import sys
# Path : pour manipuler les chemins de fichiers facilement
from pathlib import Path

# pandas : pour créer et sauvegarder le tableau de données (DataFrame)
import pandas as pd

# Chemins calculés à partir de l'emplacement du script : ça marche
# quel que soit le dossier depuis lequel on lance la commande.

# RACINE = dossier principal du projet (2 niveaux au-dessus de ce fichier)
RACINE = Path(__file__).resolve().parent.parent
# On ajoute la racine aux chemins de Python pour pouvoir importer features.py
sys.path.insert(0, str(RACINE))
# On importe la fonction qui calcule les caractéristiques et la liste de leurs noms
from features import extraire_features, NOMS_FEATURES  # noqa: E402  (P3)

# Emplacement du fichier CSV qui sera créé
CHEMIN_CSV = RACINE / "dataset" / "dataset.csv"

# Fixe le hasard : on obtient toujours les mêmes mots de passe à chaque exécution
random.seed(42)

# Nombre de mots de passe par classe : 300 x 3 = 900 lignes (dataset équilibré)
N_PAR_CLASSE = 300

# --------------------------------------------------------------------------
# 1. Ressources fictives pour fabriquer les mots de passe
# --------------------------------------------------------------------------
# Mots très utilisés (donc dangereux dans un mot de passe)
MOTS_COURANTS = [
    "password", "motdepasse", "admin", "azerty", "qwerty", "welcome",
    "bonjour", "soleil", "football", "maroc", "casablanca", "dragon",
    "master", "login", "iloveyou", "monkey", "letmein", "secret",
]
# Prénoms fictifs utilisés pour les mots de passe "personnels"
PRENOMS = ["karim", "sara", "youssef", "amina", "omar", "lina", "hamza", "nora"]
# Mots simples pour fabriquer des phrases de passe
MOTS_PHRASE = ["cheval", "nuage", "bleu", "montagne", "cafe", "riviere",
               "tigre", "lune", "jardin", "orange", "vent", "pierre"]
# Suites de touches ou de caractères faciles à deviner
SEQUENCES_CLAVIER = ["azerty", "qwerty", "qsdfgh", "wxcvbn", "123456",
                     "abcdef", "987654", "111111", "000000"]
# Symboles spéciaux utilisables dans les mots de passe forts
SYMBOLES = "!@#$%^&*()-_=+[]{};:,.?/"


# --------------------------------------------------------------------------
# 2. Règles d'étiquetage (identiques à regles_etiquetage.md)
#    Elles utilisent les colonnes de features.py (P3)
# --------------------------------------------------------------------------
def etiqueter(f: dict) -> str:
    """Donne le niveau (Faible/Moyen/Fort) à partir des caractéristiques f."""
    # Vrai si un caractère se répète 3 fois de suite ou plus (ex : "aaa")
    repetition = f["max_repetition"] >= 3
    # Vrai s'il y a une suite (ex : "123") ou un motif de clavier (ex : "azerty")
    sequence = f["a_une_suite"] == 1 or f["a_motif_clavier"] == 1
    # Vrai si au moins un motif dangereux est présent
    motif = repetition or sequence or f["a_mot_courant"] == 1

    # FAIBLE : une seule condition suffit

    # Trop court (moins de 8 caractères)
    if f["longueur"] < 8:
        return "Faible"
    # Un seul type de caractère (ex : que des minuscules)
    if f["diversite"] <= 1:
        return "Faible"
    # Mot courant et pas assez long
    if f["a_mot_courant"] == 1 and f["longueur"] < 12:
        return "Faible"
    # Motif dangereux et peu de variété de caractères
    if motif and f["diversite"] <= 2:
        return "Faible"

    # FORT : toutes les conditions doivent être réunies
    # Long (12+), varié (3 types ou plus) et sans motif dangereux
    if f["longueur"] >= 12 and f["diversite"] >= 3 and not motif:
        return "Fort"

    # MOYEN : tout le reste
    return "Moyen"


# --------------------------------------------------------------------------
# 4. Générateurs de mots de passe fictifs (variés pour couvrir tous les cas)
# --------------------------------------------------------------------------
def aleatoire(longueur, alphabet):
    """Chaîne aléatoire de la longueur demandée, avec les caractères de l'alphabet."""
    # Tire un caractère au hasard 'longueur' fois, puis les colle ensemble
    return "".join(random.choice(alphabet) for _ in range(longueur))


def capitaliser(mot):
    """Met la 1re lettre en majuscule une fois sur deux."""
    # random.random() donne un nombre entre 0 et 1 : moins de 0.5 = une chance sur deux
    return mot.capitalize() if random.random() < 0.5 else mot


def gen_faible():
    """Fabrique un mot de passe plutôt faible (type choisi au hasard)."""
    # Choisit au hasard le type de mot de passe faible à fabriquer
    t = random.choice(["court", "chiffres", "mot_courant", "mot_annee",
                       "clavier", "repete", "minuscules"])
    # Court : 3 à 7 caractères
    if t == "court":
        return aleatoire(random.randint(3, 7), string.ascii_letters + string.digits + "!@#")
    # Uniquement des chiffres
    if t == "chiffres":
        return aleatoire(random.randint(6, 10), string.digits)
    # Un mot connu, parfois avec majuscule
    if t == "mot_courant":
        return capitaliser(random.choice(MOTS_COURANTS))
    # Prénom ou mot connu suivi d'un nombre (ex : "karim1987")
    if t == "mot_annee":
        return random.choice(PRENOMS + MOTS_COURANTS) + str(random.randint(1, 2026))
    # Suite de touches, avec parfois un petit ajout à la fin
    if t == "clavier":
        return random.choice(SEQUENCES_CLAVIER) + random.choice(["", "1", "!!", "00"])
    # Même caractère répété 5 à 10 fois
    if t == "repete":
        return random.choice("abcdxyz123") * random.randint(5, 10)
    # Dernier cas : 8 à 12 minuscules seulement
    return aleatoire(random.randint(8, 12), string.ascii_lowercase)


def gen_moyen():
    """Fabrique un mot de passe de niveau moyen (type choisi au hasard)."""
    # Choisit au hasard le type de mot de passe moyen à fabriquer
    t = random.choice(["mot_chiffres", "mixte_court", "prenom_symbole",
                       "mot_maj_chiffre", "aleatoire_moyen", "phrase_courte"])
    # Un mot suivi de 3 à 5 chiffres
    if t == "mot_chiffres":
        return random.choice(MOTS_PHRASE) + aleatoire(random.randint(3, 5), string.digits)
    # Lettres (maj/min) et chiffres, 8 à 11 caractères
    if t == "mixte_court":
        return aleatoire(random.randint(8, 11), string.ascii_letters + string.digits)
    # Prénom avec majuscule + un symbole + un nombre
    if t == "prenom_symbole":
        return random.choice(PRENOMS).capitalize() + random.choice("!@#$") + str(random.randint(10, 9999))
    # Deux mots collés (le 1er avec majuscule) + un nombre
    if t == "mot_maj_chiffre":
        return random.choice(MOTS_PHRASE).capitalize() + random.choice(MOTS_PHRASE) + str(random.randint(1, 99))
    # Minuscules, chiffres et symboles "!?" : 8 à 10 caractères
    if t == "aleatoire_moyen":
        return aleatoire(random.randint(8, 10), string.ascii_lowercase + string.digits + "!?")
    # Dernier cas : trois mots collés
    return random.choice(MOTS_PHRASE) + random.choice(MOTS_PHRASE) + random.choice(MOTS_PHRASE)


def gen_fort():
    """Fabrique un mot de passe plutôt fort (type choisi au hasard)."""
    # Choisit au hasard le type de mot de passe fort à fabriquer
    t = random.choice(["aleatoire_long", "phrase_symboles", "tres_long"])
    # 12 à 18 caractères tirés de tous les types (lettres, chiffres, symboles)
    if t == "aleatoire_long":
        return aleatoire(random.randint(12, 18), string.ascii_letters + string.digits + SYMBOLES)
    # Phrase de passe : 3 mots différents
    if t == "phrase_symboles":
        # Tire 3 mots différents au hasard
        mots = random.sample(MOTS_PHRASE, 3)
        # Choisit un séparateur (ex : "-")
        sep = random.choice("-_.!#")
        # Assemble : Mot1-Mot2-Mot3-1234 (mots avec majuscule, séparés, + nombre)
        return sep.join(m.capitalize() for m in mots) + sep + str(random.randint(100, 9999))
    # Dernier cas : très long, 18 à 26 caractères variés
    return aleatoire(random.randint(18, 26), string.ascii_letters + string.digits + SYMBOLES)


# --------------------------------------------------------------------------
# 3. Construction du dataset (étiquette = résultat des règles, pas du générateur)
# --------------------------------------------------------------------------
def construire():
    """Génère des mots de passe jusqu'à avoir 300 exemples par classe."""
    # lignes : les données gardées | vus : mots de passe déjà utilisés (anti-doublon)
    lignes, vus = [], set()
    # Compte combien d'exemples on a pour chaque classe
    compteurs = {"Faible": 0, "Moyen": 0, "Fort": 0}
    # Les 3 fonctions qui fabriquent des mots de passe
    generateurs = [gen_faible, gen_moyen, gen_fort]
    # Nombre d'essais déjà faits (sécurité pour ne pas boucler à l'infini)
    tentatives = 0
    # On continue tant qu'une classe n'est pas pleine (maximum 200000 essais)
    while min(compteurs.values()) < N_PAR_CLASSE and tentatives < 200000:
        tentatives += 1
        # Choisit un générateur au hasard et fabrique un mot de passe
        mdp = random.choice(generateurs)()
        # Si on l'a déjà, on passe au suivant
        if mdp in vus:
            continue
        # Calcule les caractéristiques du mot de passe (longueur, diversité...)
        feats = extraire_features(mdp)
        # Détermine son niveau grâce aux règles
        label = etiqueter(feats)
        # Si cette classe a déjà ses 300 exemples, on ignore ce mot de passe
        if compteurs[label] >= N_PAR_CLASSE:
            continue
        # On garde ce mot de passe : on le note et on compte +1 pour sa classe
        vus.add(mdp)
        compteurs[label] += 1
        # Une ligne du dataset = mot de passe + ses caractéristiques + son niveau
        lignes.append({"mot_de_passe": mdp, **feats, "label": label})
    # Transforme la liste en tableau avec les colonnes dans le bon ordre
    df = pd.DataFrame(lignes, columns=["mot_de_passe"] + NOMS_FEATURES + ["label"])
    # Mélange les lignes (sinon elles seraient rangées au hasard des tirages)
    return df.sample(frac=1, random_state=42).reset_index(drop=True)


def verifier(df: pd.DataFrame):
    """Affiche quelques contrôles de qualité sur le dataset."""
    # Nombre total de lignes
    print("Lignes :", len(df))
    # Nombre d'exemples par classe (doit être 300 chacune)
    print("\nRépartition des classes :\n", df["label"].value_counts())
    # Nombre de cases vides (doit être 0)
    print("\nValeurs manquantes :", int(df.isna().sum().sum()))
    # Nombre de mots de passe en double (doit être 0)
    print("Doublons :", int(df["mot_de_passe"].duplicated().sum()))
    # Moyenne de chaque caractéristique par classe, pour vérifier que les classes diffèrent
    print("\nMoyennes par classe :")
    print(df.groupby("label")[["longueur", "diversite", "max_repetition",
                               "a_une_suite", "a_motif_clavier",
                               "a_mot_courant"]].mean().round(2))


# Ce bloc s'exécute seulement quand on lance ce fichier directement
if __name__ == "__main__":
    # Fabrique le dataset
    df = construire()
    # Affiche les contrôles de qualité
    verifier(df)
    # Sauvegarde le dataset dans le fichier CSV
    df.to_csv(CHEMIN_CSV, index=False, encoding="utf-8")
    print("\n", CHEMIN_CSV, "généré.")
