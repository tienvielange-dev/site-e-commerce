
from flask import Flask, render_template, request, redirect, url_for, session
import os
app.secret_key = os.environ.get("SECRET_KEY", "dev_key")
app=Flask(__name__)

app.secret_key = "kora_shop_secret_key"

# =========================
# PRODUITS
# =========================

produits = [
    {"id": 0, "nom": "Hoodie premium", "categorie": "Vêtements", "prix": 28000, "tag": "Nouveau"},
    {"id": 1, "nom": "Sneakers urbaines", "categorie": "Vêtements", "prix": 38000, "tag": "Tendance"},
    {"id": 2, "nom": "Sac à dos voyage", "categorie": "Sacs", "prix": 24000, "tag": ""},
    {"id": 3, "nom": "Sac à main en cuir", "categorie": "Sacs", "prix": 35000, "tag": "-15 %"},
    {"id": 4, "nom": "Casque Bluetooth ANC", "categorie": "Audio", "prix": 45000, "tag": "Best-seller"},
    {"id": 5, "nom": "Écouteurs sans fil", "categorie": "Audio", "prix": 19000, "tag": ""},
    {"id": 6, "nom": "Laptop 15 pouces 16 Go", "categorie": "Ordinateurs", "prix": 385000, "tag": "16 Go RAM"},
    {"id": 7, "nom": "Ultrabook alu", "categorie": "Ordinateurs", "prix": 520000, "tag": "Nouveau"},
    {"id": 8, "nom": "Smartphone Nova 5G", "categorie": "Téléphones", "prix": 165000, "tag": "5G"},
    {"id": 9, "nom": "Smartphone Nova Pro", "categorie": "Téléphones", "prix": 290000, "tag": "-10 %"},
    {"id": 10, "nom": "Montre connectée", "categorie": "Accessoires", "prix": 55000, "tag": ""},
    {"id": 11, "nom": "Lunettes de soleil", "categorie": "Accessoires", "prix": 15000, "tag": "Été"}
]

categories = [
    "Tout", "Vêtements", "Sacs", "Audio",
    "Ordinateurs", "Téléphones", "Accessoires"
]


# =========================
# PAGE D'ACCUEIL
# =========================

@app.route("/")
def accueil():

    categorie = request.args.get("categorie", "Tout")

    if categorie not in categories:
        categorie = "Tout"

    if categorie == "Tout":
        produits_affiches = produits
    else:
        produits_affiches = [
            p for p in produits
            if p["categorie"] == categorie
        ]

    panier = session.get("panier", {})

    articles = []
    total = 0
    nombre = 0

    for identifiant, quantite in panier.items():

        produit = produits[int(identifiant)]

        sous_total = produit["prix"] * quantite

        articles.append({
            "produit": produit,
            "quantite": quantite,
            "sous_total": sous_total
        })

        total += sous_total
        nombre += quantite

    return render_template(
        "index.html",
        produits=produits_affiches,
        categories=categories,
        categorie=categorie,
        articles=articles,
        total=total,
        nombre=nombre,
        panier_ouvert=request.args.get("panier") == "1",
        commande=request.args.get("commande") == "ok"
    )


# =========================
# AJOUTER AU PANIER
# =========================

@app.route("/ajouter/<int:id>", methods=["POST"])
def ajouter(id):

    if id < 0 or id >= len(produits):
        return redirect(url_for("accueil"))

    panier = session.get("panier", {})

    cle = str(id)

    panier[cle] = panier.get(cle, 0) + 1

    session["panier"] = panier

    categorie = request.form.get("categorie", "Tout")

    if categorie not in categories:
        categorie = "Tout"

    return redirect(url_for(
        "accueil",
        categorie=categorie,
        panier=1
    ))


# =========================
# MODIFIER LES QUANTITÉS
# =========================

@app.route("/modifier/<int:id>/<action>", methods=["POST"])
def modifier(id, action):

    panier = session.get("panier", {})
    cle = str(id)

    if cle in panier:

        if action == "plus":
            panier[cle] += 1

        elif action == "moins":
            panier[cle] -= 1

            if panier[cle] <= 0:
                del panier[cle]

    session["panier"] = panier

    return redirect(url_for("accueil", panier=1))


# =========================
# FERMER LE PANIER
# =========================

@app.route("/fermer")
def fermer():

    return redirect(url_for("accueil"))


# =========================
# COMMANDER
# =========================

@app.route("/commander", methods=["POST"])
def commander():

    panier = session.get("panier", {})

    if not panier:
        return redirect(url_for("accueil", panier=1))

    # Enregistrement en base de données à ajouter ultérieurement.

    session["panier"] = {}

    return redirect(url_for("accueil", commande="ok"))


# =========================
# LANCEMENT
# =========================

'''if __name__=='__main__':
    app.run(debug=True)'''