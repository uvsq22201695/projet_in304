from data import create_data, create_file, check
from tweets import Tweet

import json


def initialize(filename: str):
    """
    Fonction permettant d'initialiser les données des tweets
    :param filename: Nom du fichier json contenant les tweets
    """
    tweets = []  # Liste des tweets

    # On ouvre le fichier json et on le charge dans une liste de dictionnaire
    with open(filename, "r", encoding="UTF-8") as file:
        data = [json.loads(line) for line in file]

    # On parcourt chaque tweet
    for tweet_data in data:
        tweet = Tweet(tweet_data)  # On crée un objet Tweet
        tweet.extract_entities()  # On extrait les entités du tweet (hashtags, utilisateur mentionné, sentiment)
        tweets.append(tweet)  # On ajoute le tweet à la liste des tweets

    # On crée le dossier data s'il n'existe pas sinon on le vide
    create_file()

    # On écrit les données des tweets dans un fichier json
    create_data("zonedatterrissage", [tweet.__dict__ for tweet in tweets])

    return tweets