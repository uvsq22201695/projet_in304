import os
import json
import shutil

DIRECTORY_NAME = "data"


def create_file():
    # On crée le dossier data s'il n'existe pas sinon on le vide
    if not os.path.exists(DIRECTORY_NAME):
        os.mkdir(DIRECTORY_NAME)
    else:
        shutil.rmtree(DIRECTORY_NAME)
        os.mkdir(DIRECTORY_NAME)


def create_data(name: str, data: list):
    """
    Cette fonction permet de créer les données brutes.
    :param name: Nom du fichier
    :param data: Liste des données
    """

    # On crée un fichier qui contient les données des tweets.
    with open(f"{DIRECTORY_NAME}/{name}.json", "w", encoding="UTF-8") as file:
        json.dump(data, file, indent=4)
