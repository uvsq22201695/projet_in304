from model import make_model
from inits import *


def main():
    """
    Fonction principale
    """

    tweets = initialize("aitweets.json")  # On initialise les données des tweets

    # On crée l'interface graphique
    make_model(tweets, "aitweets.json")


if __name__ == "__main__":
    main()
