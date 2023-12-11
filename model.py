import json

import gradio as gr

from entities import count_entities, topEntities, count_tweets_per_country
from histogram import create_histogram_top
from circulardiagram import create_circular_diagram
from inits import initialize
from data import check
from carte import create_world_map

RADIO_LABEL = "Top K"
RADIO_INFO = "Cochez la case si vous souhaitez avoir le top K renseignés."
RADIO_CHOICES = ["Hashtags", "Utilisateurs mentionnés", "Utilisateurs actifs", "Topics", "Masquer"]
MAP_CHOICES = ["Afficher la carte", "Masquer"]
current_map_i = 0
SLIDER_LABEL = "K "
SLIDER_INFO = "Veuillez choisir un nombre entre 2 et 50"
SENTIMENT_CHOICES = ["Polarité", "Subjectivité", "Masquer"]

choices = {
    "Hashtags": "hashtags",
    "Utilisateurs actifs": "users",
    "Utilisateurs mentionnés": "users_mentioned",
    "Topics": "topics",
    "Polarité": "polarity",
    "Subjectivité": "subjectivity"
}

THEME = "Base"

css = """
    .inpoda_title {
        font-family: "Roboto", sans-serif;
        text-align: center;
    }
    
    .svelte-1gfkn6j {
        font-family: "Roboto", sans-serif;
        font-size: 20px;
    }
    
"""


def make_model(tweets):
    """
    Cette fonction permet de créer l'interface graphique.
    :param tweets: Liste des tweets
    """

    def init_entities():
        """
        Cette fonction permet d'initialiser un dictionnaire contenant les hashtags, utilisateurs, arobases,
        polarité, et subjectivité des tweets
        """
        entities_hashtags = count_entities(tweets, "hashtags")
        entities_users = count_entities(tweets, "users")
        entities_users_mentioned = count_entities(tweets, "arobase")
        entities_topics = count_entities(tweets, "topics")

        entities_polarity = count_entities(tweets, "polarity")
        entities_subjectivity = count_entities(tweets, "subjectivity")

        map_tweets = count_tweets_per_country(tweets)

        return {
            "hashtags": entities_hashtags,
            "users": entities_users,
            "users_mentioned": entities_users_mentioned,
            "topics": entities_topics,
            "polarity": entities_polarity,
            "subjectivity": entities_subjectivity,
            "map": map_tweets
        }

    temp = init_entities()

    with gr.Blocks(theme=THEME, css=css, title="InPoDa") as interface:
        """
        Cette "fonction" permet de créer l'interface graphique.
        """

        def change_slider(choice: str, value: int):
            """
            Cette fonction permet d'afficher le slider et l'histogramme en fonction du choix de l'utilisateur.
            :param choice: Choix de l'utilisateur
            :param value: Valeur du slider
            :return: Slider et histogramme
            """

            current_val = value if value != 0 else 10  # On initialise la valeur du slider à 10 si elle est nulle

            # On vérifie si l'utilisateur à cocher la case "Masquer"
            if choice == RADIO_CHOICES[-1]:
                return {
                    slider_hashtags: gr.Slider(visible=False),  # On cache le slider
                    plot_hashtags: gr.Plot(visible=False)  # On cache l'histogramme
                }

            # Sinon, on affiche le slider et l'histogramme correspondant à la cache cochée
            return {
                slider_hashtags: gr.Slider(2, 50, value=current_val, step=1,
                                           label=SLIDER_LABEL + choice.lower(),
                                           info=SLIDER_INFO, visible=True, interactive=True),
                plot_hashtags: gr.Plot(create_histogram_top(topEntities(current_val, temp[choices[choice]]),
                                                            choices[choice]), visible=True)
            }

        def change_histogram(choice: str, value: int):
            """
            Cette fonction permet de changer l'histogramme en fonction du choix de l'utilisateur.
            :param choice: Choix de l'utilisateur
            :param value: Valeur du slider
            :return: Histogramme
            """

            return {
                plot_hashtags: gr.Plot(create_histogram_top(topEntities(value, temp[choices[choice]]),
                                                            choices[choice]), visible=True)
            }

        def tweet_per_country():
            """
            Cette fonction permet d'afficher le nombre de tweets par pays.
            :return: Nombre de tweets par pays
            """
            global current_map_i
            l, c, t = [], [], []
            for k in temp["map"]:
                l.append(k)
                c.append(temp["map"][k][0])
                t.append(temp["map"][k][1])


            if l == []:
                return {plot_map: gr.Plot(visible=False),
                        map_btn: gr.Button(value=MAP_CHOICES[current_map_i], variant="secondary", visible=True, interactive=True)}

            if current_map_i >= 1:
                current_map_i = 0
                return {plot_map: gr.Plot(visible=False),
                        map_btn: gr.Button(value=MAP_CHOICES[current_map_i], variant="secondary", visible=True)}

            else:
                current_map_i += 1
                return {plot_map: gr.Plot(create_world_map(l, c, t), visible=True),
                        map_btn: gr.Button(value=MAP_CHOICES[current_map_i], variant="secondary", visible=True)}

        def get_number_user_publication(username: str):
            """
            Cette fonction permet d'afficher le nombre de publications d'un utilisateur.
            :param username: Nom d'utilisateur
            :return: Nombre de publications
            """

            if username is None:
                return ""

            return "L'utilisateur " + username + " a publié " + str(
                temp["users"].get(username)["occurence"]) + " fois."

        def get_number_hashtag_publication(hashtag: str):
            """
            Cette fonction permet d'afficher le nombre de publications d'un hashtag.
            :param hashtag: Hashtag
            :return: Nombre de publications
            """

            if hashtag is None:
                return ""

            return "Le hashtag " + hashtag + " a été utilisé " + str(
                temp["hashtags"].get(hashtag)["occurence"]) + " fois."

        def get_sentiment(choice: str):
            """
            Cette fonction permet d'afficher le sentiment des utilisateurs.
            :param choice: Choix de l'utilisateur
            :return: Sentiment
            """

            if choice == SENTIMENT_CHOICES[-1]:
                return {
                    sentiment_plot: gr.Plot(visible=False)
                }
            else:
                return {
                    sentiment_plot: gr.Plot(create_circular_diagram(temp[choices[choice]], "subjectivity"),
                                            visible=True)
                }

        def user_tweets(username: str):
            """
            Cette fonction permet d'afficher les tweets d'un utilisateur.
            :return: Tweets
            """

            return [[tweets[i].id, tweets[i].text] for i in range(len(tweets)) if tweets[i].user == username]

        def user_mentionned_tweets(username: str):
            """
            Cette fonction permet d'afficher les tweets où l'utilisateur est mentionné.
            :return: Tweets
            """

            return [[tweets[i].id, tweets[i].text] for i in range(len(tweets)) if username in tweets[i].arobase]

        def user_mentionned_hashtags(hashtag: str):
            """
            Cette fonction permet d'afficher les tweets où le hashtag est mentionné.
            :return: Tweets
            """

            if hashtag is None:
                return []

            return [[user] for user in temp["hashtags"][hashtag]["users_who_used"]]

        def user_mentionned_user(username: str):
            """
            Cette fonction permet d'afficher les utilisateurs mentionnés par l'utilisateur.
            :return: Tweets
            """

            if username is None:
                return []

            mention_user = []

            for user in temp["users_mentioned"]:
                if username in temp["users_mentioned"][user]["users_who_used"]:
                    if user not in mention_user:
                        mention_user.append([user])

            return mention_user

        def user_publications_clear():
            """
            Cette fonction permet d'effacer le contenu du textbox.
            :return: Textbox
            """

            return {
                user_publications_dropdown: None,
                user_publications_textbox: None
            }

        def hashtag_publications_clear():
            """
            Cette fonction permet d'effacer le contenu du textbox.
            :return: Textbox
            """

            return {
                hashtag_publications_dropdown: None,
                hashtag_publications_textbox: None
            }

        def user_tweets_clear():
            """
            Cette fonction permet d'effacer le contenu du textbox.
            :return: Textbox
            """

            return {
                user_tweets_dropdown: None,
                user_tweets_dataframe: None
            }

        def user_mentionned_tweets_clear():
            """
            Cette fonction permet d'effacer le contenu du textbox.
            :return: Textbox
            """

            return {
                user_mentionned_tweets_dropdown: None,
                user_mentionned_tweets_dataframe: None
            }

        def user_mentionned_hashtags_clear():
            """
            Cette fonction permet d'effacer le contenu du textbox.
            :return: Textbox
            """

            return {
                user_mentionned_hashtags_dropdown: None,
                user_mentionned_hashtags_dataset: []
            }

        def user_mentionned_user_clear():
            """
            Cette fonction permet d'effacer le contenu du textbox.
            :return: Textbox
            """

            return {
                user_mentionned_user_dropdown: None,
                user_mentionned_user_dataset: []
            }

        def change_file_after_submitting(file: str):
            global current_map_i
            nonlocal tweets, temp
            """
            Cette fonction permet de changer le fichier après avoir cliqué sur le bouton "Envoyez".
            :param file: Nom du fichier
            :return: Nom du fichier
            """

            if file is None:
                gr.Warning("Veuillez choisir un fichier à analyser. Restauration des données précédentes.")
                return {
                    radio_top: radio_top,
                    user_publications_dropdown: user_publications_dropdown,
                    user_publications_textbox: user_publications_textbox,
                    hashtag_publications_dropdown: hashtag_publications_dropdown,
                    hashtag_publications_textbox: hashtag_publications_textbox,
                    sentiment_radio: sentiment_radio,
                    user_tweets_dropdown: user_tweets_dropdown,
                    user_tweets_dataframe: user_tweets_dataframe,
                    user_mentionned_tweets_dropdown: user_mentionned_tweets_dropdown,
                    user_mentionned_tweets_dataframe: user_mentionned_tweets_dataframe,
                    user_mentionned_hashtags_dropdown: user_mentionned_hashtags_dropdown,
                    user_mentionned_hashtags_dataset: user_mentionned_hashtags_dataset,
                    user_mentionned_user_dropdown: user_mentionned_user_dropdown,
                    user_mentionned_user_dataset: user_mentionned_user_dataset,
                    map_btn: map_btn,
                    plot_map: plot_map,
                    file_download: file_download
                }

            # On ouvre le fichier json et on le charge dans une liste de dictionnaire
            with open(file, "r", encoding="UTF-8") as file:
                data = [json.loads(line) for line in file]

            if not check(data):
                gr.Warning("Les données ne sont pas valides. Restauration des données précédentes.")
                return {
                    radio_top: radio_top,
                    user_publications_dropdown: user_publications_dropdown,
                    user_publications_textbox: user_publications_textbox,
                    hashtag_publications_dropdown: hashtag_publications_dropdown,
                    hashtag_publications_textbox: hashtag_publications_textbox,
                    sentiment_radio: sentiment_radio,
                    user_tweets_dropdown: user_tweets_dropdown,
                    user_tweets_dataframe: user_tweets_dataframe,
                    user_mentionned_tweets_dropdown: user_mentionned_tweets_dropdown,
                    user_mentionned_tweets_dataframe: user_mentionned_tweets_dataframe,
                    user_mentionned_hashtags_dropdown: user_mentionned_hashtags_dropdown,
                    user_mentionned_hashtags_dataset: user_mentionned_hashtags_dataset,
                    user_mentionned_user_dropdown: user_mentionned_user_dropdown,
                    user_mentionned_user_dataset: user_mentionned_user_dataset,
                    map_btn: map_btn,
                    plot_map: plot_map,
                    file_download: file_download
                }
            else:
                gr.Info("Les données sont valides et en cours d'initialisation")
                tweets = initialize(data)
                temp = init_entities()
                gr.Info("Les données sont initialisées")

                current_map_i = 0

                return {
                    radio_top: gr.Radio(value="Masquer"),
                    user_publications_dropdown: gr.Dropdown(choices=list(temp["users"].keys()), value=None),
                    user_publications_textbox: None,
                    hashtag_publications_dropdown: gr.Dropdown(choices=list(temp["hashtags"].keys()), value=None),
                    hashtag_publications_textbox: None,
                    sentiment_radio: gr.Radio(value="Masquer"),
                    user_tweets_dropdown: gr.Dropdown(choices=list(temp["users"].keys()), value=None),
                    user_tweets_dataframe: None,
                    user_mentionned_tweets_dropdown: gr.Dropdown(choices=list(temp["users"].keys()), value=None),
                    user_mentionned_tweets_dataframe: None,
                    user_mentionned_hashtags_dropdown: gr.Dropdown(choices=list(temp["hashtags"].keys()), value=None),
                    user_mentionned_hashtags_dataset: [],
                    user_mentionned_user_dropdown: gr.Dropdown(choices=list(temp["users"].keys()), value=None),
                    user_mentionned_user_dataset: [],
                    map_btn: gr.Button(value=MAP_CHOICES[0], variant="secondary", visible=True, interactive=True),
                    plot_map: gr.Plot(visible=False),
                    file_download: gr.File(file_types=[".json"], value="data/zonedatterrissage.json"),
                }

        gr.Markdown("# InPoDa", elem_classes="inpoda_title")  # Titre de l'interface graphique

        f = gr.File(label="Choisissez un fichier à analyser (.json)", file_types=[".json"], value="aitweets.json")
        btn = gr.Button(value="Envoyez", variant="secondary", visible=True)

        gr.Markdown("---", elem_classes="inpoda_title")

        radio_top = gr.Radio(choices=RADIO_CHOICES, value="Masquer", label=RADIO_LABEL, info=RADIO_INFO)
        slider_hashtags = gr.Slider(visible=False)
        plot_hashtags = gr.Plot(visible=False)

        radio_top.change(change_slider, inputs=[radio_top, slider_hashtags], outputs=[slider_hashtags, plot_hashtags])
        slider_hashtags.change(change_histogram, inputs=[radio_top, slider_hashtags], outputs=plot_hashtags)

        gr.Markdown("## Carte des tweets", elem_classes="inpoda_title")
        map_btn = gr.Button(value=MAP_CHOICES[0], variant="secondary", visible=True)
        plot_map = gr.Plot(visible=False)
        map_btn.click(tweet_per_country, outputs=[plot_map, map_btn])

        gr.Markdown("## Statistiques sur le nombre de publications", elem_classes="inpoda_title")

        with gr.Row():
            user_publications_dropdown = gr.Dropdown(choices=list(temp["users"].keys()),
                                                     label="Choisissez l'utilisateur dont vous souhaitez "
                                                           "connaître le nombre de publications")
            user_publications_textbox = gr.Textbox(max_lines=1, label="Nombre de publications")
        user_publications_clearbutton = gr.ClearButton(value="Effacer", variant="secondary")

        user_publications_dropdown.select(get_number_user_publication, inputs=user_publications_dropdown,
                                          outputs=user_publications_textbox)
        user_publications_clearbutton.click(user_publications_clear, outputs=[user_publications_dropdown,
                                                                              user_publications_textbox])

        with gr.Row():
            hashtag_publications_dropdown = gr.Dropdown(choices=list(temp["hashtags"].keys()),
                                                        label="Choisissez le hashtag dont vous souhaitez connaître "
                                                              "le nombre de publications")
            hashtag_publications_textbox = gr.Textbox(max_lines=1, label="Nombre de publications")
        hashtag_publications_clearbutton = gr.ClearButton(value="Effacer", variant="secondary")

        hashtag_publications_dropdown.select(get_number_hashtag_publication, inputs=hashtag_publications_dropdown,
                                             outputs=hashtag_publications_textbox)
        hashtag_publications_clearbutton.click(hashtag_publications_clear, outputs=[hashtag_publications_dropdown,
                                                                                    hashtag_publications_textbox])

        gr.Markdown("## Analyse des sentiments des utilisateurs", elem_classes="inpoda_title")

        sentiment_radio = gr.Radio(choices=SENTIMENT_CHOICES, value="Masquer",
                                   label="Polarité ou subjectivité ?", info="Cocher la case correspondante.")
        sentiment_plot = gr.Plot(visible=False)
        sentiment_radio.change(get_sentiment, inputs=sentiment_radio, outputs=sentiment_plot)

        gr.Markdown("## Ensemble de tweets", elem_classes="inpoda_title")

        with gr.Row():
            user_tweets_dropdown = gr.Dropdown(choices=list(temp["users"].keys()),
                                               label="Choisissez l'utilisateur dont vous souhaitez connaître "
                                                     "les tweets")
            user_tweets_dataframe = gr.Dataframe(headers=["ID", "Texte"], height=250,
                                                 label="Tweet(s) de l'utilisateur")
        user_tweets_clearbutton = gr.ClearButton(value="Effacer", variant="secondary")

        user_tweets_dropdown.select(user_tweets, inputs=user_tweets_dropdown, outputs=user_tweets_dataframe)
        user_tweets_clearbutton.click(user_tweets_clear, outputs=[user_tweets_dropdown, user_tweets_dataframe])

        with gr.Row():
            user_mentionned_tweets_dropdown = gr.Dropdown(choices=list(temp["users"].keys()),
                                                          label="Choisissez l'utilisateur dont vous souhaitez "
                                                                "connaître les tweets où l'utilisateur est "
                                                                "mentionné")
            user_mentionned_tweets_dataframe = gr.Dataframe(headers=["ID", "Texte"], height=250,
                                                            label="Tweet(s) où l'utilisateur est mentionné")
        user_mentionned_tweets_clearbutton = gr.ClearButton(value="Effacer", variant="secondary")

        user_mentionned_tweets_dropdown.select(user_mentionned_tweets, inputs=user_mentionned_tweets_dropdown,
                                               outputs=user_mentionned_tweets_dataframe)
        user_mentionned_tweets_clearbutton.click(user_mentionned_tweets_clear,
                                                 outputs=[user_mentionned_tweets_dropdown,
                                                          user_mentionned_tweets_dataframe])

        gr.Markdown("## Utilisateurs ayant fait une action spécifique", elem_classes="inpoda_title")

        with gr.Row():
            user_mentionned_hashtags_dropdown = gr.Dropdown(choices=list(temp["hashtags"].keys()),
                                                            label="Choisissez le hashtag dont vous souhaitez "
                                                                  "connaître les utilisateurs l'ayant utilisé")
            user_mentionned_hashtags_dataset = gr.Dataset(components=["text"], samples=[],
                                                          label="Utilisateurs ayant utilisé le hashtag")
        user_mentionned_hashtags_clearbutton = gr.ClearButton(value="Effacer", variant="secondary")

        user_mentionned_hashtags_dropdown.select(user_mentionned_hashtags,
                                                 inputs=user_mentionned_hashtags_dropdown,
                                                 outputs=user_mentionned_hashtags_dataset)
        user_mentionned_hashtags_clearbutton.click(user_mentionned_hashtags_clear,
                                                   outputs=[user_mentionned_hashtags_dropdown,
                                                            user_mentionned_hashtags_dataset])

        with gr.Row():
            user_mentionned_user_dropdown = gr.Dropdown(choices=list(temp["users"].keys()),
                                                        label="Choisissez l'utilisateur dont vous souhaitez "
                                                              "connaître les utilisateurs qu'il a mentionné")
            user_mentionned_user_dataset = gr.Dataset(components=["text"], samples=[],
                                                      label="Utilisateurs mentionné par l'utilisateur choisi")
        user_mentionned_user_clearbutton = gr.ClearButton(value="Effacer", variant="secondary")

        user_mentionned_user_dropdown.select(user_mentionned_user, inputs=user_mentionned_user_dropdown,
                                             outputs=user_mentionned_user_dataset)
        user_mentionned_user_clearbutton.click(user_mentionned_user_clear,
                                               outputs=[user_mentionned_user_dropdown,
                                                        user_mentionned_user_dataset])

        gr.Markdown("## Télécharger zonedatterrissage.json", elem_classes="inpoda_title")
        file_download = gr.File(file_types=[".json"], value="data/zonedatterrissage.json")

        btn.click(change_file_after_submitting, inputs=[f], outputs=[radio_top,
                                                                     user_publications_dropdown,
                                                                     user_publications_textbox,
                                                                     hashtag_publications_dropdown,
                                                                     hashtag_publications_textbox,
                                                                     sentiment_radio,
                                                                     user_tweets_dropdown,
                                                                     user_tweets_dataframe,
                                                                     user_mentionned_tweets_dropdown,
                                                                     user_mentionned_tweets_dataframe,
                                                                     user_mentionned_hashtags_dropdown,
                                                                     user_mentionned_hashtags_dataset,
                                                                     user_mentionned_user_dropdown,
                                                                     user_mentionned_user_dataset,
                                                                     map_btn,
                                                                     plot_map,
                                                                     file_download])


    interface.launch(favicon_path="favicon.png")


    # countries = count_tweets_per_country(tweets)
    # l, c, t = [], [], []
    # for k in countries:
    #     l.append(k)
    #     c.append(countries[k][0])
    #     t.append(countries[k][1])
    # create_world_map(l, c, t)
