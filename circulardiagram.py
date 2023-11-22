import matplotlib.pyplot as plt

TITLE = {
    "polarity": "Diagramme circulaire du pourcentage des différentes polarités des tweets",
    "subjectivity": "Diagramme circulaire du pourcentage des différentes subjectivités des tweets"
}


def create_circular_diagram(data: dict, val: str):
    """
    Cette fonction permet de créer un diagramme circulaire des hashtags les plus utilisés.
    :param data: Dictionnaire des données
    :param val: Chaines de caractères qui contient le nom du dictionnaire
    """

    fig = plt.figure(figsize=(20, 10))
    plt.pie(list(data[k]["occurence"] for k in data.keys()), labels=list(data.keys()), autopct='%1.1f%%', shadow=True, startangle=90)
    plt.title(TITLE[val])
    fig.savefig("data/" + val + ".png")

    return fig

