def count_entities(tweets: list, entity: str) -> dict:
    """
    Cette fonction permet de retourner les entités avec leur nombre de publications.
    :param tweets: Liste des tweets
    :param entity: Chaîne de caractères de l'entité comptée
    :return entitydict: Dictionnaire des entités avec leur nombre de publications
    """

    entitydict = {}  # Dictionnaire des entités

    # On parcourt chaque tweet
    for tweet in tweets:
        # On parcourt chaque entité du tweet si on ne cherche pas d'utilisateurs
        if entity != "users":
            for elem in eval(f"tweet.{entity}"):
                count_entity(elem, entitydict, entity, tweet)
        else:
            count_entity(tweet.user, entitydict, entity, tweet)

    # On retourne les hashtags avec leur nombre de publications
    return entitydict


def count_entity(element, D: dict, entity, tweet):
    """
    Cette fonction permet de retourner un élément d'une entité.
    :param element: Variable de l'élément observé
    :param D: Dictionnaire des entités avec leur nombre de publications
    :param entity: Chaîne de caractères de l'entité comptée
    :param tweets: Liste des tweets
    :return D: Dictionnaire des entités avec leur nouveau nombre de publications
    """
    if element in D:  # Si l'élément est déjà dans le dictionnaire
        D[element]["occurence"] += 1  # On incrémente le nombre d'occurence de l'élément

        if entity in ["arobases", "users"]:  # Si l'on cherche des utilisateurs ou des arobases
            D[element]["id"].append(tweet.id)  # On ajoute l'id du tweet à la liste des id de l'élément

        if entity in ["arobases", "hashtags"]:  # Si l'on cherche des hashtags ou des arobases
            if tweet.user not in D[element][
                "users_who_used"]:  # Si l'utilisateur n'est pas déjà dans la liste des utilisateurs ayant utilisé l'élément
                D[element]["users_who_used"].append(tweet.user)  # On ajoute l'utilisateur à la liste des utilisateurs

    else:  # Sinon
        D[element] = {"occurence": 1}  # On initialise le nombre d'occurence de l'élément à 1

        if entity in ["arobases", "users"]:  # Si l'on cherche des utilisateurs ou des arobases
            D[element]["id"] = [tweet.id]  # On ajoute l'id du tweet à la liste des id de l'élément

        if entity in ["arobases", "hashtags"]:  # Si l'on cherche des hashtags ou des arobases
            D[element]["users_who_used"] = [tweet.user]  # On ajoute l'utilisateur à la liste des utilisateurs

    return D


def topEntities(k: int, entity: dict) -> dict:
    """
    Cette fonction permet de retourner les k entités les plus utilisés.
    :param k: Nombre d'entités à retourner
    :param entity: Dictionnaire des entités avec leur nombre de publications
    :return top_entities: Dictionnaire des k entités les plus utilisés
    """

    # On trie d'abord le dict hashtags par ordre décroissant
    entities = dict(sorted(entity.items(), key=lambda item: item[1]["occurence"], reverse=True))

    # On crée un dictionnaire des k hashtags les plus utilisés avec leur occurence
    top_entities = {}

    for i, e in enumerate(entities):
        if i == k:
            break
        top_entities[e] = entities[e]["occurence"]

    # On retourne les k entités les plus utilisés
    return top_entities
