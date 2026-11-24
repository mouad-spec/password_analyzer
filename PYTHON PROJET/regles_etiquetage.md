# Règles d'étiquetage des mots de passe

Catégories : **Faible**, **Moyen**, **Fort** (écriture exacte, avec majuscule initiale).
Les règles sont appliquées dans l'ordre : Faible, puis Fort, puis Moyen par défaut.
Elles utilisent les caractéristiques calculées par `features.py` (Personne 3).

## Caractéristiques utilisées

| Colonne | Définition |
|---|---|
| `longueur` | Nombre de caractères |
| `diversite` | Nombre de types présents parmi minuscules, majuscules, chiffres, symboles (de 0 à 4) |
| `max_repetition` | Longueur de la plus longue série du même caractère (aaa = 3) |
| `a_une_suite` | 1 si une suite de 3 caractères ou plus (abc, 123, cba, 321) |
| `a_motif_clavier` | 1 si 4 touches voisines du clavier (azer, qwer, rewq...) |
| `a_mot_courant` | 1 si un mot très courant est présent, y compris avec substitutions (P@ssw0rd) |

Les autres colonnes (`nb_minuscules`, `nb_majuscules`, `nb_chiffres`, `nb_symboles`, `nb_uniques`, `ratio_uniques`) sont fournies au modèle mais ne servent pas directement à l'étiquetage.

Définitions pour les règles :
- **répétition** = `max_repetition >= 3`
- **suite** = `a_une_suite = 1` OU `a_motif_clavier = 1`
- **motif prévisible** = répétition OU suite OU `a_mot_courant = 1`

## Règle 1 : Faible (une seule condition suffit)
- `longueur` < 8
- `diversite` <= 1 (un seul type de caractères)
- mot courant ET `longueur` < 12
- motif prévisible ET `diversite` <= 2

## Règle 2 : Fort (toutes les conditions)
- `longueur` >= 12
- `diversite` >= 3
- aucun motif prévisible

## Règle 3 : Moyen
Tous les autres cas.

## Remarques
- Tous les mots de passe sont **fictifs et générés aléatoirement** : aucun mot de passe réel n'est utilisé.
- L'étiquette est calculée par ces règles dans `generate_dataset.py`, jamais à la main.
