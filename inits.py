from data import *
from tweets import Tweet


def initialize(data: list):
    """
    Fonction permettant d'initialiser les données des tweets
    :param data: Liste des données
    """
    tweets = []  # Liste des tweets
    topics = [
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "neural networks",
        "data science",
        "big data",
        "data mining",
        "data analysis",
        "data visualization",
        "data engineering",
        "data modeling",
        "data analytics",
        "data management",
        "data wrangling",
        "data quality",
        "data governance",
        "data integration",
        "data architecture",
        "data lake",
        "data warehouse",
        "data catalog",
        "data pipeline",
        "data security",
        "data privacy",
        "data ethics",
        "data protection",
        "data storage",
        "data migration",
        "data virtualization",
        "data transformation",
        "data strategy",
        "data monetization",
        "data stewardship",
        "data classification",
        "data lineage",
        "data cleansing",
        "data enrichment",
        "data profiling",
        "data discovery",
        "data preparation",
        "data validation",
        "space",
        "research",
        "science",
        "technology",
        "innovation",
        "engineering",
        "robotics",
        "programming",
        "prosthetics",
        "nanotechnology",
        "biotechnology",
        "medicine",
        "healthcare",
        "education",
        "automation",
        "autonomous",
        "self-driving",
        "self-learning",
        "self-aware",
        "smart",
        "intelligent",
        "sports",
        "entertainment",
        "gaming",
        "virtual reality",
        ]

    # On parcourt chaque tweet
    for tweet_data in data:
        tweet = Tweet(tweet_data)  # On crée un objet Tweet
        tweet.find_topics(topics)
        tweet.extract_entities()
        tweets.append(tweet)  # On ajoute le tweet à la liste des tweets

    # On crée le dossier data s'il n'existe pas sinon on le vide
    create_file()

    # On écrit les données des tweets dans un fichier json
    create_data("zonedatterrissage", [tweet.__dict__ for tweet in tweets])

    return tweets
