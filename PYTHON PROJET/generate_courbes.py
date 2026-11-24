"""
generate_courbes.py
Crée les graphiques d'évaluation du modèle (matrice de confusion, courbes).
On n'a pas besoin de features.py : les caractéristiques sont déjà dans dataset.csv.

Utilisation :  python generate_courbes.py
Sortie : dossier graphiques/ (images PNG)
"""
from pathlib import Path

# matplotlib : pour dessiner les graphiques
import matplotlib
matplotlib.use("Agg")  # mode sans fenêtre : on sauvegarde juste les images
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (ConfusionMatrixDisplay, auc, confusion_matrix,
                             roc_curve)
from sklearn.model_selection import (learning_curve, train_test_split,
                                     validation_curve)
from sklearn.preprocessing import label_binarize
from sklearn.tree import DecisionTreeClassifier

# --- Chemins -------------------------------------------------------------
DOSSIER = Path(__file__).resolve().parent
SORTIE = DOSSIER / "graphiques"
# Crée le dossier de sortie s'il n'existe pas
SORTIE.mkdir(exist_ok=True)

# Les 3 classes, dans l'ordre
CLASSES = ["Faible", "Moyen", "Fort"]

# --- 1. Chargement des données (même découpage que train_model.py) -------
df = pd.read_csv(DOSSIER / "dataset.csv")
# X = toutes les colonnes de caractéristiques (on enlève le mot de passe et le label)
X = df.drop(columns=["mot_de_passe", "label"])
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# Même modèle que dans train_model.py
modele = DecisionTreeClassifier(max_depth=6, random_state=42)
modele.fit(X_train, y_train)
y_pred = modele.predict(X_test)

# --- 2. Matrice de confusion (nombres) -----------------------------------
fig, ax = plt.subplots(figsize=(5.5, 4.5))
ConfusionMatrixDisplay.from_predictions(
    y_test, y_pred, labels=CLASSES, cmap="Blues", ax=ax)
ax.set_title("Matrice de confusion (jeu de test)")
ax.set_xlabel("Classe prédite")
ax.set_ylabel("Classe réelle")
fig.tight_layout()
fig.savefig(SORTIE / "1_matrice_confusion.png", dpi=150)
plt.close(fig)

# --- 3. Matrice de confusion normalisée (pourcentages par ligne) ---------
fig, ax = plt.subplots(figsize=(5.5, 4.5))
ConfusionMatrixDisplay.from_predictions(
    y_test, y_pred, labels=CLASSES, normalize="true",
    cmap="Greens", values_format=".0%", ax=ax)
ax.set_title("Matrice de confusion normalisée")
ax.set_xlabel("Classe prédite")
ax.set_ylabel("Classe réelle")
fig.tight_layout()
fig.savefig(SORTIE / "2_matrice_confusion_normalisee.png", dpi=150)
plt.close(fig)

# --- 4. Courbes ROC (une par classe) -------------------------------------
# On transforme les labels en 0/1 pour chaque classe
y_bin = label_binarize(y_test, classes=CLASSES)
# Probabilités prédites, colonnes dans l'ordre de modele.classes_
proba = modele.predict_proba(X_test)
ordre = [list(modele.classes_).index(c) for c in CLASSES]

fig, ax = plt.subplots(figsize=(6, 5))
for i, c in enumerate(CLASSES):
    fpr, tpr, _ = roc_curve(y_bin[:, i], proba[:, ordre[i]])
    ax.plot(fpr, tpr, lw=2, label=f"{c} (AUC = {auc(fpr, tpr):.3f})")
# Ligne diagonale = hasard
ax.plot([0, 1], [0, 1], "k--", lw=1, label="Hasard")
ax.set_xlabel("Taux de faux positifs")
ax.set_ylabel("Taux de vrais positifs")
ax.set_title("Courbes ROC par classe")
ax.legend(loc="lower right")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(SORTIE / "3_courbes_roc.png", dpi=150)
plt.close(fig)

# --- 5. Courbe d'apprentissage -------------------------------------------
# Montre la précision selon la quantité de données d'entraînement
tailles, sc_train, sc_val = learning_curve(
    DecisionTreeClassifier(max_depth=6, random_state=42), X, y,
    cv=5, train_sizes=np.linspace(0.1, 1.0, 8), random_state=42, shuffle=True)

fig, ax = plt.subplots(figsize=(6.5, 4.5))
ax.plot(tailles, sc_train.mean(axis=1), "o-", label="Entraînement")
ax.plot(tailles, sc_val.mean(axis=1), "o-", label="Validation croisée")
# Zone = écart-type entre les 5 plis
ax.fill_between(tailles, sc_val.mean(axis=1) - sc_val.std(axis=1),
                sc_val.mean(axis=1) + sc_val.std(axis=1), alpha=0.2)
ax.set_xlabel("Nombre d'exemples d'entraînement")
ax.set_ylabel("Précision (accuracy)")
ax.set_title("Courbe d'apprentissage")
ax.set_ylim(0.8, 1.02)
ax.legend(loc="lower right")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(SORTIE / "4_courbe_apprentissage.png", dpi=150)
plt.close(fig)

# --- 6. Courbe de validation selon la profondeur de l'arbre --------------
profondeurs = range(1, 13)
sc_train, sc_val = validation_curve(
    DecisionTreeClassifier(random_state=42), X, y,
    param_name="max_depth", param_range=profondeurs, cv=5)

fig, ax = plt.subplots(figsize=(6.5, 4.5))
ax.plot(profondeurs, sc_train.mean(axis=1), "o-", label="Entraînement")
ax.plot(profondeurs, sc_val.mean(axis=1), "o-", label="Validation croisée")
# Ligne verticale = profondeur choisie dans le projet
ax.axvline(6, color="gray", ls="--", label="max_depth choisi (6)")
ax.set_xlabel("Profondeur maximale de l'arbre (max_depth)")
ax.set_ylabel("Précision (accuracy)")
ax.set_title("Courbe de validation")
ax.legend(loc="lower right")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(SORTIE / "5_courbe_validation_profondeur.png", dpi=150)
plt.close(fig)

# --- 7. Importance des caractéristiques ----------------------------------
imp = pd.Series(modele.feature_importances_, index=X.columns).sort_values()
fig, ax = plt.subplots(figsize=(7, 5))
ax.barh(imp.index, imp.values, color="#3b7dd8")
ax.set_xlabel("Importance")
ax.set_title("Importance des caractéristiques")
ax.grid(axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig(SORTIE / "6_importance_caracteristiques.png", dpi=150)
plt.close(fig)

# Résumé dans la console
print("Accuracy test :", round((y_pred == y_test).mean(), 3))
print(confusion_matrix(y_test, y_pred, labels=CLASSES))
print("Graphiques enregistrés dans :", SORTIE)
