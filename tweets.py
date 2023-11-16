import re
from textblob import TextBlob
from random import choices

# Dictionnaire des utilisateurs avec leur poids
users_weight = {
    "IainLJBrown": 15.0,
    "byLilyV": 15.0,
    "andi_staub": 15.0,
    "Kbuxton90": 9.0,
    "elonmusk": 8.0,
    "YouTube": 5.0,
    "unikuma_yukkuri": 5.0,
    "TechTweet24h": 5.0,
    "DeepLearn007": 5.0,
    "JolaBurnett": 5.0,
    "TechXplore_com": 4.0,
    "ILASColumbia": 3.0,
    "Indika_AI": 2.0,
    "Entrepreneur": 2.0,
    "Kevin_Jackson": 1.0,
    "data_nerd": 1.0
}


def chose_username() -> str:
    """
    Cette fonction permet de choisir un nom d'utilisateur.
    :return username: Nom d'utilisateur
    """

    # On convertit les valeurs du dictionnaire en liste
    users_weight_list = list(users_weight.values())

    # On retourne un nom d'utilisateur aléatoire en fonction de la liste des utilisateurs
    return choices(list(users_weight.keys()), weights=users_weight_list, k=1)[0]


class Tweet:
    """
    Cette classe permet de créer un objet tweet.
    """

    cleaned_text: str  # Liste des mots du tweet

    def __init__(self, tweet_data: dict):
        """
        Constructeur de la classe Tweet
        :param tweet_data: Dictionnaire contenant les données du tweet
        """

        self.id = tweet_data["id"]
        self.user = chose_username()
        self.text = tweet_data["TweetText"]
        self.clean_text(["#", "@"])
        self.hashtags = []
        self.arobase = []
        # self.topics = []
        self.feelings = self.calculate_sentiment()

    def calculate_sentiment(self) -> str:
        """
        Cette fonction permet de calculer le sentiment du tweet.
        :return bool: True si sentiment positif, False sinon
        """
        return "Négatif" if TextBlob(self.text).sentiment.polarity < 0 else "Positif"

    def extract_entities(self):
        """
        Cette fonction permet d'extraire les entités du tweet (hashtags, arobases)
        """

        # On sépare le texte en liste de mots
        text = self.cleaned_text.split()

        # On parcourt chaque mot du tweet
        for word in text.copy():
            if word[0] not in ["#", "@"] or word[1:] == "":
                continue
            if word[0] == "#":  # Si le mot commence par un #
                self.hashtags.append(word[1:])  # On ajoute le mot sans le # à la liste des hashtags
            elif word[0] == "@":  # Si le mot commence par un @
                self.arobase.append(word[1:])  # On ajoute le mot sans le @ à la liste des arobases
            text.remove(word)

        self.cleaned_text = " ".join(text)

        # doc = nlp(self.cleaned_text)
        # for token in doc:
        #     if "subj" in token.dep_:
        #         subtree = list(token.subtree)
        #         start = subtree[0].i
        #         end = subtree[-1].i + 1
        #         self.topics.append(doc[start:end])

    def clean_text(self, excepted_char: list):
        """
        Cette fonction permet de nettoyer le texte du tweet.
        :param excepted_char: Liste des caractères à ne pas remplacer
        """

        cleaned_text = self.text.strip()

        # On remplace les "RT" et les hyperliens par des espaces
        cleaned_text = re.sub("http://\S+|https://\S+", "", cleaned_text)
        cleaned_text = cleaned_text.replace("RT ", "")

        # On remplace les caractères spéciaux par des espaces sauf si ceux-ci sont dans excepted_char
        cleaned_text = re.sub(fr"[^\w\s{''.join(excepted_char)}]+", "", cleaned_text)

        self.cleaned_text = cleaned_text
