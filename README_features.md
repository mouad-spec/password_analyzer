# Module 3 : Feature Engineering (Password_Analyzer)

## 1. Objectif du module

Ce module transforme un mot de passe (texte) en un ensemble de **12 caractéristiques numériques** utilisables par le modèle de Machine Learning (Scikit-learn). Il fournit deux fonctions : une pour un seul mot de passe (application Flask), une pour un lot de mots de passe (entraînement du modèle sur le dataset).

Fichiers du module :
- `features.py` : le code d'extraction
- `test_features.py` : les tests automatiques
- `README_features.md` : ce document

## 2. Les 12 caractéristiques

L'ordre des colonnes est **figé** dans la liste `NOMS_FEATURES` de `features.py`. Il ne doit jamais changer sans ré-entraîner le modèle.

| # | Colonne | Définition | Type / plage | Exemple | Justification |
|---|---|---|---|---|---|
| 1 | `longueur` | Nombre total de caractères, espaces inclus | Entier ≥ 0 | `Mouad123@ ` → 10 | Plus le mot de passe est long, plus le nombre de combinaisons à tester augmente |
| 2 | `nb_minuscules` | Nombre de lettres minuscules | Entier ≥ 0 | `Ensab123@ ` → 4 | Mesure l'usage de l'alphabet de base |
| 3 | `nb_majuscules` | Nombre de lettres majuscules | Entier ≥ 0 | `Ensab123@ ` → 1 | Élargit l'espace de recherche d'un attaquant |
| 4 | `nb_chiffres` | Nombre de chiffres | Entier ≥ 0 | `Ensab123@ ` → 3 | Mesure l'usage des chiffres, souvent ajoutés en fin de mot |
| 5 | `nb_symboles` | Nombre de caractères qui ne sont ni lettre ni chiffre (espace compris) | Entier ≥ 0 | `Ensab123@ ` → 2 | Les symboles sont rares dans les mots de passe faibles |
| 6 | `diversite` | Nombre de catégories présentes parmi minuscules, majuscules, chiffres, symboles | Entier de 0 à 4 | `Ensab123@ ` → 4 | Un mélange de catégories complique une attaque |
| 7 | `nb_uniques` | Nombre de caractères différents | Entier ≥ 0 | `aaaa` → 1 | Peu de caractères différents indique un mot de passe pauvre |
| 8 | `ratio_uniques` | `nb_uniques` divisé par `longueur` (0 si le mot de passe est vide), arrondi à 4 décimales | Décimal de 0 à 1 | `aaaa` → 0.25 | Compare la variété à la longueur : un mot long mais répétitif reste faible |
| 9 | `max_repetition` | Longueur de la plus longue série du même caractère | Entier ≥ 0 | `aaaa` → 4 | Les répétitions (`aaaa`, `1111`) sont des habitudes très courantes |
| 10 | `a_une_suite` | 1 si une suite de 3 caractères ou plus, croissante ou décroissante, de lettres ou de chiffres est présente, sinon 0 | 0 ou 1 | `abc` → 1, `aba` → 0 | Les suites (`abc`, `123`, `987`) sont testées en priorité par les attaquants |
| 11 | `a_motif_clavier` | 1 si un enchaînement de 4 touches voisines d'une ligne de clavier est présent (sens normal ou inverse), sinon 0 | 0 ou 1 | `Ensab_qwerty` → 1 | `azerty` et `qwerty` figurent dans toutes les listes de mots de passe fréquents |
| 12 | `a_mot_courant` | 1 si un mot de la liste des mots courants est présent, y compris avec substitutions de caractères, sinon 0 | 0 ou 1 | `P@ssw0rd` → 1 | Les substitutions classiques (`@` pour a, `0` pour o) n'arrêtent pas un attaquant |

## 3. Choix techniques

- **Espace = symbole** : tout caractère qui n'est ni une lettre ni un chiffre est compté comme symbole, y compris l'espace.
- **Suites** : seuil de **3** caractères. Une série doit garder le **même sens** (+1 ou -1) et rester du **même type** (lettres avec lettres, chiffres avec chiffres). Ainsi `aba` et `9:` ne sont pas des suites.
- **Motifs clavier** : seuil de **4** touches consécutives, dans les deux sens, sur les lignes `azertyuiop`, `qsdfghjklm`, `wxcvbn`, `qwertyuiop`, `asdfghjkl`, `zxcvbnm` et `1234567890`. Le seuil de 3 a été écarté car il crée des faux positifs (« ert » dans « expert », « ope » dans « open »).
- **Casse ignorée** : pour les suites, les motifs clavier et les mots courants, le mot de passe est converti en minuscules avant l'analyse.
- **Substitutions** pour les mots courants : `@`→a, `0`→o, `3`→e, `$`→s, `5`→s, `4`→a, `1`→i. Le mot de passe est testé sous sa forme d'origine et sous sa forme transformée.
- **Entrée invalide** (chaîne vide, `None`, nombre, case vide d'un CSV) : traitée comme une chaîne vide, donc toutes les features valent 0, sans erreur.
- **Colonnes liées** : `longueur`, `nb_uniques` et `ratio_uniques` sont corrélées. Un arbre de décision s'en accommode, mais cela est à garder en tête pour l'interprétation de l'importance des features.
- **Précalcul** : les morceaux de clavier sont calculés une seule fois à l'import du fichier, pas à chaque appel.

## 4. Limites connues

- La liste `MOTS_COURANTS` est **courte** : un mot courant absent de la liste n'est pas détecté. Elle peut être complétée avec des mots issus du dataset.
- Les suites ne détectent que les écarts de ±1 (pas `acegi` ni `13579`).
- Les caractères accentués comptent comme lettres, mais ne sont pas traités dans les suites ni dans les motifs clavier.
- Les substitutions peuvent créer de rares faux positifs (par exemple `1` transformé en `i`).
- Ces features mesurent la **structure** d'un mot de passe, pas sa **réputation** : un mot de passe structurellement correct mais présent dans une fuite de données reste faible.

## 5. Mode d'emploi

### Pour P1 (application Flask) : un seul mot de passe

```python
import pandas as pd
from features import extraire_features, NOMS_FEATURES

features = extraire_features(mot_de_passe_saisi)        # dictionnaire plat
ligne = pd.DataFrame([features], columns=NOMS_FEATURES) # une ligne, colonnes dans le bon ordre
# prediction = modele.predict(ligne)
```

### Pour P4 (entraînement) : un lot de mots de passe

```python
from features import extraire_features_lot, NOMS_FEATURES

X = extraire_features_lot(df["password"])   # une ligne par mot de passe, 12 colonnes
# entraîner le modèle sur X
```

Règles importantes :
- Utiliser **le même module** pour l'entraînement et pour la prédiction.
- Ne jamais réordonner ni renommer les colonnes. Si une feature est ajoutée ou modifiée, mettre à jour `NOMS_FEATURES` **et ré-entraîner le modèle**.

## 6. Lancer les tests

Placer `features.py` et `test_features.py` dans le même dossier, puis exécuter :

    python test_features.py

Le programme affiche le nom de chaque test suivi de `OK`, puis `Tous les tests passent.`
