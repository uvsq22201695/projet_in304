# from tweets import Tweet
# # Cellule qui gère les fonctions sur les topics
# 
# def count_topics(tweets: list) -> dict:
#     """
#     Cette fonction permet de retourner les topics avec leur nombre de publications.
#     :param tweets: Liste des tweets
#     :return topics: Dictionnaire des topics avec leur nombre de publications
#     """
# 
#     topics = {}  # Dictionnaire des topics
# 
#     # On parcourt chaque tweet
#     for tweet in tweets:
#         # On parcourt chaque topic du tweet
#         for topic in tweet.topics:
#             if topic in topics:  # Si le topic est déjà dans le dictionnaire
#                 topics[topic]["occurence"] += 1  # On incrémente le nombre d'occurence du topic
#                 topics[topic]["id"].append(tweet.id)  # On ajoute l'id du tweet à la liste des id de l'arobase
#             else:  # Sinon
#                 topics[topic] = {
#                     "occurence": 1,
#                     "id": [tweet.id]
#                 }
# 
#     # On retourne les topics avec leur nombre de publications
#     return topics
# 
# 
# def top_topics(k: int, topics: dict) -> list:
#     """
#     Cette fonction permet de retourner les k topics les plus utilisés.
#     :param k: Nombre de topics à retourner
#     :param topics: Liste des topics avec leur nombre de publications
#     :return top_topics: Liste des k topics les plus utilisés
#     """
# 
#     # On retourne les k topics les plus utilisés
#     return sorted(topics, key=lambda topic: topics[topic]["occurence"], reverse=True)[:k]