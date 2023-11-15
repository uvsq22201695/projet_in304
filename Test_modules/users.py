from tweets import Tweet

def count_user(tweets: list) -> dict:
    """
    Cette fonction permet de retourner les utilisateurs avec leur nombre de publications.
    :param tweets: Liste des tweets
    :return users: Dictionnaire des utilisateurs avec leur nombre de publications
    """

    users = {}  # Dictionnaire des utilisateurs

    # On parcourt chaque tweet
    for tweet in tweets:
        if tweet.user in users:  # Si l'utilisateur est déjà dans le dictionnaire
            users[tweet.user]["occurence"] += 1  # On incrémente le nombre d'occurence de l'utilisateur
            users[tweet.user]["id"].append(tweet.id)  # On ajoute l'id du tweet à la liste des id de l'utilisateur
        else:  # Sinon
            users[tweet.user] = {  # On ajoute l'utilisateur au dictionnaire
                "occurence": 1,
                "id": [tweet.id]
            }
    
    # On retourne les utilisateurs avec leur nombre de publications
    return users

def top_users(k: int, users: dict) -> list:
    """
    Cette fonction permet de retourner les k utilisateurs les plus actifs.
    :param k: Nombre d'utilisateurs à retourner
    :param users: Liste des utilisateurs avec leur nombre de publications
    :return top_users: Liste des k utilisateurs les plus actifs
    """

    # On retourne les k utilisateurs les plus actifs
    return sorted(users, key=lambda user: users[user]["occurence"], reverse=True)[:k]