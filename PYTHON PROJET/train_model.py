"""
train_model.py  -  Personne 4 (Module 4 : Machine Learning)
Entraîne un Decision Tree pour classer les mots de passe (Faible / Moyen / Fort).

Les caractéristiques viennent de features.py (Personne 3) : on réutilise sa
liste NOMS_FEATURES pour garantir le même ordre partout.

Utilisation :  python training/train_model.py   (depuis n'importe quel dossier)
Entrée : dataset/dataset.csv      Sortie : model/password_model.pkl
"""
# sys : permet de modifier les chemins où Python cherche les modules
import sys
# Path : pour manipuler les chemins de fichiers facilement
from pathlib import Path

# joblib : pour sauvegarder le modèle dans un fichier
import joblib
# pandas : pour lire le CSV et manipuler les tableaux
import pandas as pd
# Outils pour mesurer la qualité du modèle
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
# train_test_split : coupe les données en 2 parties | cross_val_score : validation croisée
from sklearn.model_selection import cross_val_score, train_test_split
# L'arbre de décision et une fonction pour afficher ses règles en texte
from sklearn.tree import DecisionTreeClassifier, export_text

# --- Chemins calculés depuis l'emplacement du script ---------------------
# RACINE = dossier principal du projet
RACINE = Path(__file__).resolve().parent.parent
# On ajoute la racine aux chemins de Python pour pouvoir importer features.py
sys.path.insert(0, str(RACINE))
# Liste des noms de caractéristiques, dans le bon ordre
from features import NOMS_FEATURES  # noqa: E402  (P3)

# Fichier d'entrée (données) et fichier de sortie (modèle entraîné)
CHEMIN_DATASET = RACINE / "dataset" / "dataset.csv"
CHEMIN_MODELE = RACINE / "model" / "password_model.pkl"

# Les 3 classes, dans l'ordre utilisé pour la matrice de confusion
CLASSES = ["Faible", "Moyen", "Fort"]

# --- 1. Chargement du dataset -------------------------------------------
# Lit le fichier CSV dans un tableau
df = pd.read_csv(CHEMIN_DATASET)

# X = les données d'entrée que le modèle utilise pour décider
X = df[NOMS_FEATURES]     # caractéristiques (ordre de P3)
# y = la réponse que le modèle doit apprendre à prédire
y = df["label"]           # étiquette à prédire

# --- 2. Séparation entraînement / test ----------------------------------
# 80 % des données pour apprendre, 20 % pour tester le modèle sur des exemples jamais vus
# (stratify=y garde les mêmes proportions de classes dans les deux parties)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
print("Entraînement :", len(X_train), "lignes | Test :", len(X_test), "lignes")

# --- 3. Création et entraînement du modèle ------------------------------
# Crée l'arbre de décision ; max_depth=6 limite sa taille pour éviter qu'il
# apprenne les données par cœur
modele = DecisionTreeClassifier(max_depth=6, random_state=42)
# Entraînement : l'arbre apprend les règles à partir des données d'entraînement
modele.fit(X_train, y_train)

# --- 4. Évaluation -------------------------------------------------------
# Le modèle prédit le niveau des mots de passe de test
y_pred = modele.predict(X_test)
# Accuracy = pourcentage de bonnes prédictions
print("\nPrécision (accuracy) sur le test :", round(accuracy_score(y_test, y_pred), 3))
# Détail par classe : précision, rappel, f1-score
print("\nRapport de classification :\n", classification_report(y_test, y_pred, digits=3))
# Matrice de confusion : montre quelles classes sont confondues entre elles
print("Matrice de confusion (lignes = réel, colonnes = prédit) :")
print(pd.DataFrame(confusion_matrix(y_test, y_pred, labels=CLASSES),
                   index=CLASSES, columns=CLASSES))

# Validation croisée : on teste le modèle sur 5 découpages différents du dataset
# pour vérifier que le bon score n'est pas dû au hasard
scores = cross_val_score(DecisionTreeClassifier(max_depth=6, random_state=42), X, y, cv=5)
print("\nValidation croisée (5 plis) :", scores.round(3), "| moyenne :", round(scores.mean(), 3))

# Importance de chaque caractéristique dans les décisions de l'arbre (du plus au moins important)
importances = pd.Series(modele.feature_importances_, index=NOMS_FEATURES).sort_values(ascending=False)
print("\nImportance des caractéristiques :\n", importances.round(3))
# Affiche les règles de l'arbre sous forme de texte lisible (3 niveaux max)
print("\nRègles apprises par l'arbre :\n", export_text(modele, feature_names=NOMS_FEATURES, max_depth=3))

# --- 5. Sauvegarde du modèle --------------------------------------------
# Crée le dossier model/ s'il n'existe pas encore
CHEMIN_MODELE.parent.mkdir(exist_ok=True)
# Sauvegarde le modèle ET la liste des features, pour garder le même ordre à la prédiction
joblib.dump({"modele": modele, "features": NOMS_FEATURES}, CHEMIN_MODELE)
print("Modèle sauvegardé :", CHEMIN_MODELE)
