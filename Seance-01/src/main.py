#coding:utf8

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

def listedesterritoires(territoiretest, exportationUSD, importationUSD):
    listedesterritoires = [[territoiretest[0], 0]]
    pos = 0
    for element in range(0,len(territoiretest)):
        if territoiretest[element] != listedesterritoires[pos][0]:
            listedesterritoires.append([territoiretest[element], element])
            pos += 1
    lignes = []
    for element in range(1,len(listedesterritoires)):
        lignes.append(listedesterritoires[element][1] - 1)
    lignes.append(len(territoiretest))
    liste = []
    for element in range(0,len(listedesterritoires)):
        liste.append([listedesterritoires[element][0], listedesterritoires[element][1], lignes[element]])
    totalparterritoire = []
    for element in range(0,len(liste)):
        totalparterritoire.append([liste[element][0], exportationUSD[liste[element][1]:liste[element][2]].sum(), importationUSD[liste[element][1]:liste[element][2]].sum()])
    return totalparterritoire

def nettoyage(colonne):
    colonne2 = []
    for element in colonne:
        if element == 'Sans objet' or element =='-':
            colonne2.append(float(0))
        else:
            colonne2.append(float(element))
    return colonne2

def getliste(territoiretest):
    listedesterritoires = [[territoiretest[0], 0]]
    pos = 0
    for element in range(0,len(territoiretest)):
        if territoiretest[element] != listedesterritoires[pos][0]:
            listedesterritoires.append([territoiretest[element], element])
            pos += 1
    lignes = []
    for element in range(1,len(listedesterritoires)):
        lignes.append(listedesterritoires[element][1] - 1)
    lignes.append(len(territoiretest))
    liste = []
    for element in range(0,len(listedesterritoires)):
        liste.append([listedesterritoires[element][0], listedesterritoires[element][1], lignes[element]])
    return liste

# Question 4
print("Question 4")
# Source des données : https://www.cepii.fr/CEPII/en/bdd_modele/bdd_modele_item.asp?id=37
with open("./data/Produits-alimentaires-2024.csv", "r", encoding="utf-8") as fichier:
    contenu = pd.read_csv(fichier)

# Question 5
print("Question 5")
print(pd.DataFrame(contenu))
# Question 6
print("Question 6")
print("Nombre de lignes :", len(contenu))
print("Nombre de colonnes :", len(contenu.columns))
# Question 7
print("Question 7")
print(contenu.head())
# Question 8
print("Question 8")
print(contenu.dtypes)
# Contenu des colonnes
# "year" : année
# "origin_id" : territoire de référence
# "dest_id" : territoire partenaire
# "Dist_VO (km)" : distance intercentroïde entre les deux territoires
# "hs92_Section_id" : code Section du produit
# "hs92_HS02_id" : code 2-digit du produit
# "hs92_HS04_id" : code 4-digit du produit
# "hs92_HS06_id" : code 6-digit du produit
# "export_val" : valeur des exportations du territoire de référence vers le territoire partenaire en dollars courants
# "import_val" : valeur des importations du territoire partenaire vers le territoire de référence en dollars courants
# "export_ton" : valeur des exportations du territoire de référence vers le territoire partenaire en tonnes
# "import_ton" : valeur des importations du territoire partenaire vers le territoire de référence en tonnes

# Question 9
print("Question 9")
exportations = contenu["export_ton"]
importations = contenu["import_ton"]

print(exportations.head())
print(importations.head())
# Question 10
print("Question 10")
exportations_nombres = pd.to_numeric(exportations, errors="coerce")
importations_nombres = pd.to_numeric(importations, errors="coerce")

print("Effectif des exportations :", exportations_nombres.count())
print("Effectif des importations :", importations_nombres.count())
# Question 11
print("Question 11")
# Appliquer la fonction listedesterritoires(...) sur vos colonnes ici
territoires = listedesterritoires(
    contenu["origin_id"],
    contenu["export_val"],
    contenu["import_val"]
)
liste_pays = []

for pays in contenu["origin_id"].unique():
    liste_pays.append(pays)

print("Nombre de territoires :", len(liste_pays))
for pays in liste_pays:
    donnees_pays = contenu[contenu["origin_id"] == pays]

    total_exportations = donnees_pays["export_val"].sum()
    total_importations = donnees_pays["import_val"].sum()

    print(pays, total_exportations, total_importations)
    plt.figure()
    plt.bar(
        ["Exportations", "Importations"],
        [total_exportations, total_importations]
    )
    plt.title("Commerce extérieur - " + pays)
    plt.ylabel("Valeur en USD")
    plt.savefig("img/" + pays + ".png")
    plt.close()
# Questions 12 et 14
print("Questions 12 et 14")
# Application la fonction nettoyage(...) sur vos colonnes ici
distance = nettoyage(contenu["Dist_VO (km)"])
export_usd = nettoyage(contenu["export_val"])
import_usd = nettoyage(contenu["import_val"])
export_tonnes = nettoyage(contenu["export_ton"])
import_tonnes = nettoyage(contenu["import_ton"])
import_tonnes = nettoyage(contenu["import_ton"])

donnees2titre = [
    "distance",
    "export_val_2",
    "import_val_2",
    "export_ton_2",
    "import_ton_2"
]

donnees2 = pd.DataFrame({
    donnees2titre[0]: distance,
    donnees2titre[1]: export_usd,
    donnees2titre[2]: import_usd,
    donnees2titre[3]: export_tonnes,
    donnees2titre[4]: import_tonnes
})

print(donnees2.head())

# Construire la liste des territoires
liste = getliste(contenu["origin_id"])

# Mettre le code nouveau DataFrame ici et appeler la liste donnees2

# Compléter la boucle à partir des différents éléments précédents. Le nom des listes est celle proposée dans les commentaires.
parametres = []
quartiles = []
deciles = []

for element in range(0, len(donnees2.columns)):
    parametres2 = []
    distanceinterquartile = []
    distanceinterdecile = []

    for element2 in range(0, len(liste)):
        codeiso = liste[element2][0]
        data2 = donnees2.iloc[liste[element2][1]:liste[element2][2], element]

        moyenne = data2.mean().round(2)
        mediane = data2.median().round(2)
        mode = data2.mode().iloc[0].round(2)
        ecarttype = data2.std().round(2)
        ecartabsolumoyen = (data2 - data2.mean()).abs().mean().round(2)
        etendue = (data2.max() - data2.min()).round(2)

        parametres2.append([
            codeiso, moyenne, mediane, mode,
            ecarttype, ecartabsolumoyen, etendue
        ])
        quartile = data2.quantile([0.25, 0.75])
        distanceinterquartile.append([codeiso, round(quartile[0.75] - quartile[0.25], 2)])

        decile = data2.quantile([0.1, 0.9])
        distanceinterdecile.append([codeiso, round(decile[0.9] - decile[0.1], 2)])
    parametres.append(parametres2)
    quartiles.append(distanceinterquartile)
    deciles.append(distanceinterdecile)

# Question 13
print("Question 13")
print(parametres)
# Question 14
# Question 14 : calculs realises dans la boucle precedente

# Question 15
print("Question 15")

import os

os.makedirs("img", exist_ok=True)

for colonne in donnees2.columns:
    plt.figure(figsize=(8, 5))
    plt.boxplot(donnees2[colonne].dropna())
    plt.title("Boîte à moustaches - " + colonne)
    plt.ylabel(colonne)
    plt.savefig("img/boxplot_" + colonne + ".png")
    plt.close()

# Question 16
print("Question 16")
# Source des données : BDCOM, https://www.apur.org/fr/open-data-cartes/open-data/base-donnees-commerces-parisiens
with open("./data/restaurants-paris-2023.csv", "r", encoding="utf-8") as fichier:
    contenu2 = pd.read_csv(fichier)

# Question bonus
print("Question bonus")


# Question 17
print("Question 17")

surfaces = pd.to_numeric(contenu2["surf"], errors="coerce")

categorie1 = 0
categorie2 = 0
categorie3 = 0

for surface in surfaces:
    if surface == 1:
        categorie1 += 1
    elif surface == 2:
        categorie2 += 1
    elif surface == 3:
        categorie3 += 1

print("Code 1 :", categorie1)
print("Code 2 :", categorie2)
print("Code 3 :", categorie3)
