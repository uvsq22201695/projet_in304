from data import *
from tweets import Tweet
import gradio as gr

import json


def initialize(data: list):
    """
    Fonction permettant d'initialiser les données des tweets
    :param data: Liste des données
    """
    tweets = []  # Liste des tweets

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
