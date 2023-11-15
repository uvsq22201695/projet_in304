from tweets import Tweet
# Cellule qui gère les fonctions sur les arobases

def count_arobases(tweets: list) -> dict:
    """
    Cette fonction permet de retourner les arobases avec leur nombre de publications.
    :param tweets: Liste des tweets
    :return arobases: Dictionnaire des k arobase les plus utilisés
    """

    arobases = {}  # Dictionnaire de l'arobase

    # On parcourt chaque tweet
    for tweet in tweets:
        # On parcourt chaque arobase du tweet
        for arobase in tweet.arobase:
            if arobase in arobases:  # Si l'arobase est déjà dans le dictionnaire
                arobases[arobase]["occurence"] += 1  # On incrémente le nombre d'occurence de l'arobase
                arobases[arobase]["id"].append(tweet.id)  # On ajoute l'id du tweet à la liste des id de l'arobase
                if tweet.user not in arobases[arobase]["users_who_mentionned"]:  # Si l'utilisateur n'est pas déjà dans la liste
                    arobases[arobase]["users_who_mentionned"].append(tweet.user)  # On ajoute l'utilisateur à la liste des utilisateurs
            else:  # Sinon
                # On ajoute l'arobase au dictionnaire
                arobases[arobase] = {
                    "occurence": 1,
                    "id": [tweet.id],
                    "users_who_mentionned": [tweet.user]
                }

    # On retourne les arobases avec leur nombre de publications
    return arobases


def top_arobases(k: int, arobases: dict) -> list:
    """
    Cette fonction permet de retourner les k arobase les plus utilisés.
    :param k: Nombre d'arobases à retourner
    :param arobases: Liste des arobases avec leur nombre de publications
    :return top_arobases: Liste des k arobase les plus utilisés
    """

    # On retourne les k arobase les plus utilisés
    return sorted(arobases, key=lambda arobase: arobases[arobase]["occurence"], reverse=True)[:k]


def tweetid_arobases(user: str, arobases: dict) -> list:
    """
    Cette fonction permet de retourner les id des tweets qui ont utilisé un arobas donné.
    :param user: Arobase à rechercher
    :param arobases: Liste des arobases avec leur nombre de publications
    :return tweetid_arobases: Liste des id des tweets qui ont utilisé l'arobase
    """

    # On retourne les id des tweets qui ont utilisé l'arobase
    return arobases[user]["id"]