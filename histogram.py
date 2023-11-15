import matplotlib.pyplot as plt
# from hashtags import *
# from arobases import *
# from topics import *
# from users import *
from entities import *

# # Cellule qui gère les données graphiques

def create_histogram_topk(data: dict, val: str):
    """
    Cette fonction permet de créer un histogramme des hashtags les plus utilisés.
    :param val: Chaines de caractères qui contient le nom du dictionnaire
    :param data: Dictionnaire des données
    """
    # On crée un histogramme des hashtags les plus utilisés.
    fig = plt.figure(figsize=(20, 10))
    plt.bar(list(key for key in data.keys() if key != "id"), list(value for key,value in data.items() if key != "id"))

    plt.title(f"Histogramme des {val} les plus utilisés" if val != "users" else "Histogramme des utilisateurs ayant le plus écrit")
    plt.xlabel(val[0].upper()+val[1:] if val != "users" else "Noms d'utilisateurs")
    plt.ylabel("Nombre de publications")
    return fig
