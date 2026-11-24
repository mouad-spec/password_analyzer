# Rapport d'évaluation du modèle (Personne 4)

## Modèle
- Algorithme : Decision Tree (`DecisionTreeClassifier`, Scikit-learn), `max_depth=6`, `random_state=42`
- Apprentissage supervisé, 3 classes (Faible, Moyen, Fort)
- Entrées : les 12 caractéristiques de `features.py` (`NOMS_FEATURES`, ordre figé)

## Données
- 900 mots de passe fictifs, 300 par classe
- Séparation : 80 % entraînement (720 lignes), 20 % test (180 lignes), stratifiée par classe

## Résultats sur le jeu de test
- Précision globale (accuracy) : **99,4 %**
- Validation croisée à 5 plis : moyenne **99,1 %**

| Classe | Précision | Rappel | F1 |
|---|---|---|---|
| Faible | 1,000 | 0,983 | 0,992 |
| Moyen | 0,984 | 1,000 | 0,992 |
| Fort | 1,000 | 1,000 | 1,000 |

Matrice de confusion (lignes = réel, colonnes = prédit) :

| | Faible | Moyen | Fort |
|---|---|---|---|
| Faible | 59 | 1 | 0 |
| Moyen | 0 | 60 | 0 |
| Fort | 0 | 0 | 60 |

Une seule erreur sur 180 : un mot de passe Faible prédit Moyen.

## Caractéristiques les plus importantes
nb_uniques (36,5 %), diversite (28,0 %), longueur (21,8 %), a_mot_courant (6,7 %), a_une_suite (2,3 %), nb_chiffres et max_repetition (2,0 % chacune). `nb_uniques` est très liée à la longueur, ce qui explique sa première place.

## Interprétation et limites
- Les étiquettes sont produites par des règles : le modèle les redécouvre, d'où la précision très élevée. Cela confirme que le dataset est cohérent, pas que le modèle mesure la « vraie » force d'un mot de passe.
- Le dataset est synthétique : pas de vrais mots de passe ni de vraies attaques.
- Améliorations possibles : cas limites ou bruit, autres profondeurs, forêt aléatoire.

## Fichiers
`training/train_model.py`, `model/password_model.pkl` (modèle + liste ordonnée des caractéristiques), `training/test_prediction.py`.
