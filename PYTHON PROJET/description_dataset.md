# Description du dataset

- **Fichier** : `dataset/dataset.csv` (UTF-8, séparateur virgule)
- **Taille** : 900 lignes, 14 colonnes
- **Origine** : données synthétiques générées par `dataset/generate_dataset.py` (graine 42, reproductible)
- **Caractéristiques** : calculées par `features.py` (Personne 3), donc identiques à celles utilisées par l'application
- **Équilibre** : 300 mots de passe par classe (Faible, Moyen, Fort)
- **Qualité** : 0 valeur manquante, 0 doublon

## Colonnes
`mot_de_passe`, puis les 12 caractéristiques de `NOMS_FEATURES` dans cet ordre :
`longueur, nb_minuscules, nb_majuscules, nb_chiffres, nb_symboles, diversite, nb_uniques, ratio_uniques, max_repetition, a_une_suite, a_motif_clavier, a_mot_courant`, puis `label`.

- Variable cible : `label` (Faible / Moyen / Fort)
- Variables explicatives : les 12 caractéristiques (`mot_de_passe` ne sert pas à l'entraînement)

## Moyennes par classe
| Classe | Longueur | Diversité | Répétition max | Suite | Motif clavier | Mot courant |
|---|---|---|---|---|---|---|
| Faible | 9,26 | 1,43 | 2,03 | 0,06 | 0,05 | 0,14 |
| Moyen | 9,74 | 2,76 | 1,31 | 0,01 | 0,00 | 0,00 |
| Fort | 19,06 | 3,79 | 1,29 | 0,00 | 0,00 | 0,00 |

## Limites
Le dataset est synthétique et étiqueté par des règles : le modèle apprend ces règles, pas la « vraie » robustesse face à un attaquant. Cela convient à un objectif pédagogique de sensibilisation.
