import os
import joblib
import pandas as pd
from flask import Flask, render_template, request, jsonify
from features import extraire_features

app = Flask(__name__)

# Chargement du modèle IA (fichier fourni par la personne 4)
CHEMIN_MODELE = "model/password_model.pkl"

if os.path.exists(CHEMIN_MODELE):
    paquet_modele = joblib.load(CHEMIN_MODELE)
    modele_ia = paquet_modele["modele"]
    colonnes_modele = paquet_modele.get("features")
    print("Modèle IA chargé.")
else:
    modele_ia = None
    colonnes_modele = None
    print("Pas encore de modèle : niveau fictif utilisé.")


# Prédit le niveau du mot de passe avec le modèle IA
def predire_niveau(mdp):
    if modele_ia is None:
        return "Moyen"                                  # niveau fictif
    caracteristiques = extraire_features(mdp)           # texte → dictionnaire
    X = pd.DataFrame([caracteristiques])                # dictionnaire → tableau
    if colonnes_modele is not None:
        X = X.reindex(columns=colonnes_modele, fill_value=0)
    return str(modele_ia.predict(X)[0])                 # prédiction → textes

# Génère des conseils de sécurité adaptés au mot de passe
def generer_recommandations(mdp):
    recommandations = []

    if len(mdp) < 12:
        recommandations.append("Utilisez au moins 12 caractères.")
    if not any(c.isupper() for c in mdp):
        recommandations.append("Ajoutez des lettres majuscules.")
    if not any(c.islower() for c in mdp):
        recommandations.append("Ajoutez des lettres minuscules.")
    if not any(c.isdigit() for c in mdp):
        recommandations.append("Ajoutez des chiffres.")
    if not any(not c.isalnum() for c in mdp):
        recommandations.append("Ajoutez des symboles (!, @, #...).")

    # Si aucun problème n'a été trouvé
    if len(recommandations) == 0:
        recommandations.append("Très bon mot de passe ! Utilisez-le pour un seul site.")

    return recommandations
# Page 1 : la page d'accueil
@app.route("/")
def accueil():
    return render_template("index.html")
# Page 2 : la page du projet
@app.route("/projet")
def projet():
    return "Ce projet analyse la force des mots de passe avec l'IA."
# Page 3 : la page des conseils
@app.route("/conseils")
def conseils():
    return "Conseil :utilisez au moins 12 caractères."
# API (POST) : reçoit un mot de passe et renvoie le résultat en JSON
@app.route("/api/analyser",methods=["POST"])
def analyser():
    # 1. Recevoir : lire le mot de passe envoyé
    donnees = request.get_json(silent=True)

    # Vérification 1 : est-ce qu'on a reçu un mot de passe ?
    if not donnees or "password" not in donnees:
        return jsonify({"erreur": "Aucun mot de passe reçu."}), 400

    mdp = donnees["password"]

    # Vérification 2 : est-ce que le mot de passe est vide ?
    if mdp.strip() == "":
        return jsonify({"erreur": "Le mot de passe est vide."}), 400
    
    # 2. Traiter : niveau prédit par l'IA + conseils de sécurité
    resultat = {
        "niveau": predire_niveau(mdp),
        "recommandations": generer_recommandations(mdp)
    }
    
    # 3. Répondre : renvoyer le résultat en JSON
    return jsonify(resultat)
if __name__=="__main__":
    app.run(debug=True , use_reloader=False)