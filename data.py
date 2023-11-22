import os
import json
import shutil

DIRECTORY_NAME = "data"


def create_file():
    """
    Cette fonction permet de créer le dossier qui contiendra les données brutes.
    """

    if os.path.exists(DIRECTORY_NAME):
        shutil.rmtree(DIRECTORY_NAME)

    os.mkdir(DIRECTORY_NAME)


def create_data(name: str, data: list):
    """
    Cette fonction permet de créer les données brutes.
    :param name: Nom du fichier
    :param data: Liste des données
    """

    with open(f"{DIRECTORY_NAME}/{name}.json", "w", encoding="UTF-8") as file:
        json.dump(data, file, indent=4)
