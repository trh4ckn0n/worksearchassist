import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import openai

# Charger les variables d'environnement
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nom = request.form["nom"]
        poste = request.form["poste"]
        secteur = request.form["secteur"]
        competences = request.form["competences"]
        entreprise = request.form.get("entreprise", "")
        type_lettre = request.form["type_lettre"]

        # Adapter le ton et la structure selon le type
        if type_lettre == "lettre de motivation":
            intro = f"""
Rédige une **lettre de motivation** professionnelle, personnalisée, pour un poste de {poste} dans le secteur {secteur}.
Le ton doit être motivé, formel, structuré, et montrer un fort intérêt pour ce poste spécifique."""
        else:
            intro = f"""
Rédige une **candidature spontanée** proactive, convaincante, pour un poste de {poste} dans le secteur {secteur}.
Le candidat ne répond pas à une offre : il souhaite démontrer la valeur qu'il peut apporter à l'entreprise."""

        prompt = f"""
Tu es un expert RH chargé d'aider les candidats à rédiger leur lettre.

{intro}
Nom du candidat : {nom}
Compétences principales : {competences}
{f"Entreprise ciblée : {entreprise}." if entreprise else ""}

Structure la lettre avec une belle introduction, un développement clair et une conclusion efficace.
Utilise un ton fluide, professionnel et accrocheur. Ne dépasse pas 400 mots.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )

        texte_genere = response.choices[0].message.content.strip()
        return render_template("result.html", lettre=texte_genere)

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
