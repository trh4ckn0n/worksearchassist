import os
from flask import Flask, render_template, request
from dotenv import load_dotenv
import openai

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

        # Définir l'intro selon le type de lettre
        if type_lettre == "lettre de motivation":
            intro = f"Rédige une lettre de motivation pour un poste de {poste} dans le secteur {secteur}."
        elif type_lettre == "candidature spontanée":
            intro = f"Rédige une candidature spontanée pour un poste de {poste} dans le secteur {secteur}."

        # Construction du prompt
        prompt = f"""
Tu es un assistant RH. {intro}
Le candidat s'appelle {nom}.
Voici ses compétences : {competences}.
{f"Il souhaite postuler chez {entreprise}." if entreprise else ""}
Fais une lettre professionnelle, motivée, fluide et adaptée à la situation.
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
    app.run(debug=False, host="0.0.0.0", port=port)
