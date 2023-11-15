import os
import json
import shutil


# Cellule qui gère les données brutes

def create_file():
    # On crée le dossier data s'il n'existe pas sinon on le vide
    if not os.path.exists("data"):
        os.mkdir("data")
    else:
        shutil.rmtree("data")
        os.mkdir("data")
        
def create_data(name: str, data : list):
    """
    Cette fonction permet de créer les données brutes.
    :param name: Nom du fichier
    :param data: Liste des données
    """

    # On crée un fichier qui contient les données des tweets.
    with open(f"data/{name}.json", "w", encoding="UTF-8") as file:
        json.dump(data, file, indent=4)
