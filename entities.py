from tweets import Tweet

USERS = "users"
HASHTAGS = "hashtags"
AROBASE = "arobase"
OCCURENCE = "occurence"
ID = "id"
USERS_WHO_USED = "users_who_used"


def count_entities(tweets: list, entity_type: str) -> dict:
    """
    Cette fonction permet de retourner les entités avec leur nombre de publications.
    :param tweets: Liste des tweets
    :param entity_type: Chaîne de caractères de l'entité comptée
    :return entity_dict: Dictionnaire des entités avec leur nombre de publications
    """

    entity_dict = {}  # Dictionnaire des entités

    for tweet in tweets:

        if entity_type == USERS:
            entity_dict = count_entity(tweet.user, entity_dict, entity_type, tweet)
        else:
            for elem in eval(f"tweet.{entity_type}"):
                entity_dict = count_entity(elem, entity_dict, entity_type, tweet)

    return entity_dict


def count_entity(entity: str, entity_dict: dict, entity_type: str, tweet: Tweet):
    """
    Cette fonction permet de retourner un élément d'une entité.
    :param entity: Variable de l'élément observé
    :param entity_dict: Dictionnaire des entités avec leur nombre de publications
    :param entity_type: Chaîne de caractères de l'entité comptée
    :param tweet: Liste des tweets
    :return entity_dict: Dictionnaire des entités avec leur nouveau nombre de publications
    """

    if entity in entity_dict:
        entity_dict[entity][OCCURENCE] += 1

        if entity_type in (AROBASE, USERS):
            entity_dict[entity][ID].append(tweet.id)

        if entity_type in (AROBASE, HASHTAGS):
            if tweet.user not in entity_dict[entity][USERS_WHO_USED]:
                entity_dict[entity][USERS_WHO_USED].append(tweet.user)

    else:
        entity_dict[entity] = {OCCURENCE: 1}

        if entity_type in (AROBASE, USERS):
            entity_dict[entity][ID] = [tweet.id]

        if entity_type in (AROBASE, HASHTAGS):
            entity_dict[entity][USERS_WHO_USED] = [tweet.user]

    return entity_dict


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
