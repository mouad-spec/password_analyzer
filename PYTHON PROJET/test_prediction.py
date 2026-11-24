"""Test rapide : charge le modèle .pkl et prédit quelques mots de passe,
en utilisant extraire_features de features.py (P3)."""
# sys : permet de modifier les chemins où Python cherche les modules
import sys
# Path : pour manipuler les chemins de fichiers facilement
from pathlib import Path

# joblib : pour recharger le modèle sauvegardé
import joblib
# pandas : pour mettre les données dans un tableau, comme à l'entraînement
import pandas as pd

# RACINE = dossier principal du projet
RACINE = Path(__file__).resolve().parent.parent
# On ajoute la racine aux chemins de Python pour pouvoir importer features.py
sys.path.insert(0, str(RACINE))
# Fonction qui calcule les caractéristiques d'un mot de passe
from features import extraire_features  # noqa: E402  (P3)

# Charge le fichier .pkl : il contient le modèle entraîné et la liste des features
paquet = joblib.load(RACINE / "model" / "password_model.pkl")

# Teste 5 mots de passe, du plus faible au plus fort
for mdp in ["abc", "password123", "P@ssw0rd", "Karim2024", "Tr0ub4dor&3xK!pq"]:
    # Calcule les caractéristiques du mot de passe (longueur, diversité...)
    f = extraire_features(mdp)
    # Met les valeurs dans le même ordre qu'à l'entraînement, sinon le modèle se trompe
    X = pd.DataFrame([[f[c] for c in paquet["features"]]], columns=paquet["features"])
    # Prédit le niveau et l'affiche à côté du mot de passe
    print(f"{mdp:20s} -> {paquet['modele'].predict(X)[0]}")
