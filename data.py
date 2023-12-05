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


def check(data: list):
    """
    Cette fonction permet de vérifier si les données sont valides, c'est-à-dire si dans le fichier json il y a bien :
    - Un champ "TweetText" qui contient le texte du tweet
    - Un champ "id" qui contient l'id du tweet
    :param data: Dictionnaire contenant les données
    """

    # On parcourt chaque tweet
    for tweet in data:
        # On vérifie si le tweet contient le champ "TweetText" et "id"
        if "TweetText" not in tweet.keys() or "id" not in tweet.keys():
            return False

    return True
