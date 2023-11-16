import matplotlib.pyplot as plt

Y_LABEL = "Nombre de publications"
X_LABEL = {
    "hashtags": "Hashtags",
    "users": "Noms d'utilisateurs",
    "users_mentioned": "Noms des utilisateurs mentionnés"
}
TITLE = {
    "hashtags": "Histogramme des hashtags les plus utilisés",
    "users": "Histogramme des utilisateurs étant le plus actif",
    "users_mentioned": "Histogramme des utilisateurs mentionnés le plus souvent"
}


def create_histogram_top(data: dict, val: str):
    """
    Cette fonction permet de créer un histogramme des hashtags les plus utilisés.
    :param data: Dictionnaire des données
    :param val: Chaines de caractères qui contient le nom du dictionnaire
    """

    fig = plt.figure(figsize=(20, 10))
    plt.bar(list(data.keys()), list(data.values()))
    plt.title(TITLE[val])
    plt.xlabel(X_LABEL[val])
    plt.ylabel(Y_LABEL)

    return fig
