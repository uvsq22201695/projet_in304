# Cellule qui gère les imports
import json
import spacy
from model import *
from gestion_fichiers import *

# nlp = spacy.load('en_core_web_sm')

# Cellule qui gère la fonction main

def main(filename: str):
    """
    Fonction principale
    :param filename: Nom du fichier json  
    """

    tweets = []  # Liste des tweets

    # On ouvre le fichier json et on le charge dans une liste de dictionnaire
    with open(filename, "r", encoding="UTF-8") as file:
        data = [json.loads(line) for line in file]

    # On parcourt chaque tweet
    for tweet_data in data:
        tweet = Tweet(tweet_data)  # On crée un objet Tweet
        tweet.extract_entities()  # On extrait les entités du tweet (hashtags, arobase, sentiment)
        tweets.append(tweet)  # On ajoute le tweet à la liste des tweets
        
    # On crée le dossier data s'il n'existe pas sinon on le vide
    create_file()

    # On écrit les données des tweets dans un fichier json
    create_data("zonedatterrissage", [tweet.__dict__ for tweet in tweets])  

    make_model(tweets)


if __name__ == "__main__":
    main("aitweets.json")
