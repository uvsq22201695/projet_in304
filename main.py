from model import make_model
from inits import *


def main():
    """
    Fonction principale
    """

    # On ouvre le fichier json et on le charge dans une liste de dictionnaire
    with open("aitweets.json", "r", encoding="UTF-8") as file:
        data = [json.loads(line) for line in file]

    if not check(data):
        return "Les données d'initialisation ne sont pas valides"

    tweets = initialize(data)  # On initialise les données des tweets

    # On crée l'interface graphique
    make_model(tweets)


if __name__ == "__main__":
    main()