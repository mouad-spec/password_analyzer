# Documentation de l'API — Analyseur de mots de passe


## Lancer le serveur

```
pip install -r requirements.txt
python app.py
```

Le serveur démarre sur : http://127.0.0.1:5000

## Routes disponibles

| Méthode | Route            | Description                               |
|---------|------------------|-------------------------------------------|
| GET     | `/`              | Affiche la page d'accueil (index.html)    |
| POST    | `/api/analyser`  | Analyse un mot de passe et renvoie du JSON |

## Route `POST /api/analyser`

### Requête envoyée par le frontend

```json
{
    "password": "soleil123"
}
```

### Réponse en cas de succès (code 200)

```json
{
    "niveau": "Faible",
    "recommandations": [
        "Utilisez au moins 12 caractères.",
        "Ajoutez des lettres majuscules.",
        "Ajoutez des symboles (!, @, #...)."
    ]
}
```

- `niveau` : `"Faible"`, `"Moyen"` ou `"Fort"` (prédit par le modèle IA)
- `recommandations` : liste de conseils de sécurité

### Réponses en cas d'erreur (code 400)

| Cas                         | Réponse                                        |
|-----------------------------|------------------------------------------------|
| Aucune donnée ou pas de `password` | `{"erreur": "Aucun mot de passe reçu."}`  |
| Mot de passe vide           | `{"erreur": "Le mot de passe est vide."}`      |

## Codes HTTP utilisés

| Code | Signification                              |
|------|--------------------------------------------|
| 200  | Succès                                     |
| 400  | Requête incorrecte (données invalides)     |
| 405  | Méthode non autorisée (ex. GET sur l'API)  |

## Exemple de test en Python

```python
import requests
reponse = requests.post("http://127.0.0.1:5000/api/analyser",
                        json={"password": "soleil123"})
print(reponse.status_code, reponse.json())
```

## Sécurité

- Le mot de passe est envoyé uniquement avec **POST** (jamais dans l'URL).
- Les données reçues sont **vérifiées** avant traitement.
- Le mot de passe n'est **ni enregistré ni affiché** par le serveur.
- Le modèle `.pkl` est chargé uniquement depuis le projet (source de confiance).