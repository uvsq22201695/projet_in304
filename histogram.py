import matplotlib.pyplot as plt
from hashtags import *
from arobases import *
from topics import *
from users import *

# # Cellule qui gère les données graphiques

def create_histogram_topk(data: dict, val: str):
    """
    Cette fonction permet de créer un histogramme des hashtags les plus utilisés.
    :param val: Chaines de caractères qui contient le nom du dictionnaire
    :param data: Dictionnaire des données
    """
    
    # On crée un histogramme des hashtags les plus utilisés.
    fig = plt.figure(figsize=(20, 10))
    plt.bar(list(data.keys()), list(data.values()))

    plt.title(f"Histogramme des {val} les plus utilisés")
    plt.xlabel(val)
    plt.ylabel("Nombre de publications")
    return fig