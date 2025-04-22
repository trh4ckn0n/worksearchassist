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

        prompt = f"""
Tu es un assistant RH. Génère une {type_lettre} pour un candidat nommé {nom},
visant un poste de {poste} dans le secteur {secteur}.
Voici ses compétences principales : {competences}.
{f"L'entreprise visée est {entreprise}." if entreprise else ""}
Fais une lettre professionnelle, motivée, et personnalisée.
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
