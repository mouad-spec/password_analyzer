// Quand on clique sur "Analyser"
document.getElementById("formulaire").addEventListener("submit", async function (event) {
    // 1. Empêcher la page de se recharger
    event.preventDefault();

    // 2. Récupérer le mot de passe tapé
    const mdp = document.getElementById("password").value;

    // 3. Envoyer le mot de passe à l'API Flask (POST + JSON)
    const reponse = await fetch("/api/analyser", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password: mdp })
    });

    // 4. Lire la réponse JSON
    const donnees = await reponse.json();
    const zone = document.getElementById("resultat");

    // 5a. En cas d'erreur (code 400) : afficher le message d'erreur
    if (!reponse.ok) {
        zone.textContent = donnees.erreur;
        return;
    }

    // 5b. Sinon (code 200) : afficher le niveau et les conseils
    let html = "<h2>Niveau : " + donnees.niveau + "</h2><ul>";
    for (const conseil of donnees.recommandations) {
        html += "<li>" + conseil + "</li>";
    }
    html += "</ul>";
    zone.innerHTML = html;
});