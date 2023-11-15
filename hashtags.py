from tweets import Tweet
# Cellule qui gère les fonctions sur les hashtags

def count_hashtags(tweets: list) -> dict:
    """
    Cette fonction permet de retourner les hashtags avec leur nombre de publications.
    :param tweets: Liste des tweets
    :return hashtags: Dictionnaire des hashtags avec leur nombre de publications
    """

    hashtags = {}  # Dictionnaire des hashtags

    # On parcourt chaque tweet
    for tweet in tweets:
        # On parcourt chaque hashtag du tweet
        for hashtag in tweet.hashtags:
            if hashtag in hashtags:  # Si le hashtag est déjà dans le dictionnaire
                hashtags[hashtag]["occurence"] += 1  # On incrémente le nombre d'occurence du hashtag
                if tweet.user not in hashtags[hashtag]["users_who_used"]:  # Si l'utilisateur n'est pas déjà dans la liste
                    hashtags[hashtag]["users_who_used"].append(tweet.user)  # On ajoute l'utilisateur à la liste des utilisateurs
            else:  # Sinon
                hashtags[hashtag] = {  # On ajoute le hashtag au dictionnaire
                    "occurence": 1,
                    "users_who_used": [tweet.user]
                }

    # On retourne les hashtags avec leur nombre de publications
    return hashtags


def topHashtags(k: int, hashtags: dict) -> dict:
    """
    Cette fonction permet de retourner les k hashtags les plus utilisés.
    :param k: Nombre de hashtags à retourner
    :param hashtags: Liste des hashtags avec leur nombre de publications
    :return top_hashtags: Dictionnaire des k hashtags les plus utilisés
    """

    # On trie d'abord le dict hashtags par ordre décroissant
    hashtags = dict(sorted(hashtags.items(), key=lambda item: item[1]["occurence"], reverse=True))
    
    # On crée un dictionnaire des k hashtags les plus utilisés avec leur occurence
    top_hashtags = {}
    
    for i, hashtag in enumerate(hashtags):
        if i == k:
            break
        top_hashtags[hashtag] = hashtags[hashtag]["occurence"]
        
    # On retourne les k hashtags les plus utilisés
    return top_hashtags
    