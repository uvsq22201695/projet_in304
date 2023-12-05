import gradio as gr

from entities import count_entities, topEntities
from histogram import create_histogram_top
from circulardiagram import create_circular_diagram
from inits import initialize

RADIO_LABEL = "Top K"
RADIO_INFO = "Cochez la case si vous souhaitez avoir le top K renseignés."
RADIO_CHOICES = ["Hashtags", "Utilisateurs mentionnés", "Utilisateurs actifs", "Masquer"]
SLIDER_LABEL = "K "
SLIDER_INFO = "Veuillez choisir un nombre entre 2 et 50"
SENTIMENT_CHOICES = ["Polarité", "Subjectivité", "Masquer"]

choices = {
    "Hashtags": "hashtags",
    "Utilisateurs actifs": "users",
    "Utilisateurs mentionnés": "users_mentioned",
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


def make_model(tweets, filename: str):
    """
    Cette fonction permet de créer l'interface graphique.
    :param tweets: Liste des tweets
    :param filename: Nom du fichier
    """
    actual_file = filename

    def init_entities():
        """
        Cette fonction permet d'initialiser un dictionnaire contenant les hashtags, utilisateurs, arobases,
        polarité, et subjectivité des tweets
        """
        entities_hashtags = count_entities(tweets, "hashtags")
        entities_users = count_entities(tweets, "users")
        entities_users_mentioned = count_entities(tweets, "arobase")
        entities_polarity = count_entities(tweets, "polarity")
        entities_subjectivity = count_entities(tweets, "subjectivity")

        return {
            "hashtags": entities_hashtags,
            "users": entities_users,
            "users_mentioned": entities_users_mentioned,
            "polarity": entities_polarity,
            "subjectivity": entities_subjectivity
        }

    temp = init_entities()

    # On crée l'interface graphique
    with gr.Blocks(theme=THEME, css=css, title="InPoDa") as interface:

        gr.Markdown("# InPoDa", elem_classes="inpoda_title")  # Titre de l'interface graphique

        # On charge un différent fichier lorsque l'utilisateur le demande
        def change_file_after_submitting(file: str):
            nonlocal actual_file, tweets, temp
            """
            Cette fonction permet de changer le fichier après avoir cliqué sur le bouton "Envoyez".
            :param file: Nom du fichier
            :return: Nom du fichier
            """

            if file is not None:
                actual_file = file
                tweets = initialize(actual_file)
                temp = init_entities()

        f = gr.File(label="Choisissez un fichier à analyser (.json)", file_types=[".json"], visible=True)
        btn = gr.Button(value="Envoyez", variant="secondary", visible=True)

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

        radio_top = gr.Radio(choices=RADIO_CHOICES, value="Masquer", label=RADIO_LABEL, info=RADIO_INFO)
        slider_hashtags = gr.Slider(visible=False)  # On crée le slider et on le cache
        plot_hashtags = gr.Plot(visible=False)  # On crée l'histogramme et on le cache

        # On regarde si une action a été effectuée sur le radio ou le slider
        radio_top.change(change_slider, inputs=[radio_top, slider_hashtags], outputs=[slider_hashtags, plot_hashtags])
        slider_hashtags.change(change_histogram, inputs=[radio_top, slider_hashtags], outputs=plot_hashtags)

        gr.Markdown("## Statistiques sur le nombre de publications", elem_classes="inpoda_title")

        gr.Interface(get_number_user_publication,
                     gr.Dropdown(choices=list(temp["users"].keys()),
                                 label="Choisissez l'utilisateur dont vous souhaitez connaître le nombre de "
                                       "publications"),
                     gr.Textbox(max_lines=1),
                     live=True,
                     allow_flagging="never"
                     )

        gr.Interface(get_number_hashtag_publication,
                     gr.Dropdown(choices=list(temp["hashtags"].keys()),
                                 label="Choisissez le hashtag dont vous souhaitez connaître le nombre de "
                                       "publications"),
                     gr.Textbox(max_lines=1),
                     live=True,
                     allow_flagging="never"
                     )

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

        gr.Markdown("## Analyse des sentiments des utilisateurs", elem_classes="inpoda_title")

        sentiment_radio = gr.Radio(choices=SENTIMENT_CHOICES, value="Masquer",
                                   label="Polarité ou subjectivité ?", info="Cocher la case correspondante.")
        sentiment_plot = gr.Plot(visible=False)
        sentiment_radio.change(get_sentiment, inputs=sentiment_radio, outputs=sentiment_plot)

        def user_tweets(username: str):
            """
            Cette fonction permet d'afficher les tweets d'un utilisateur.
            :return: Tweets
            """

            return [[tweets[i].id, tweets[i].text] for i in range(len(tweets)) if tweets[i].user == username]

        gr.Markdown("## Ensemble de tweets", elem_classes="inpoda_title")

        gr.Interface(user_tweets,
                     gr.Dropdown(choices=list(temp["users"].keys()),
                                 label="Choisissez l'utilisateur dont vous souhaitez connaître les tweets"),
                     gr.Dataframe(headers=["ID", "Texte"], height=250, show_label=False, label=""),
                     live=True,
                     allow_flagging="never"
                     )

        def user_mentionned_tweets(username: str):
            """
            Cette fonction permet d'afficher les tweets où l'utilisateur est mentionné.
            :return: Tweets
            """

            return [[tweets[i].id, tweets[i].text] for i in range(len(tweets)) if username in tweets[i].arobase]

        gr.Interface(user_mentionned_tweets,
                     gr.Dropdown(choices=list(temp["users"].keys()),
                                 label="Choisissez l'utilisateur dont vous souhaitez connaître les tweets où "
                                       "l'utilisateur est mentionné"),
                     gr.Dataframe(headers=["ID", "Texte"], height=250, show_label=False, label=""),
                     live=True,
                     allow_flagging="never"
                     )

        def user_mentionned_hashtags(hashtag: str):
            """
            Cette fonction permet d'afficher les tweets où le hashtag est mentionné.
            :return: Tweets
            """

            return [[user] for user in temp["hashtags"][hashtag]["users_who_used"]]

        gr.Interface(user_mentionned_hashtags,
                     gr.Dropdown(choices=list(temp["hashtags"].keys()),
                                 label="Choisissez le hashtag dont vous souhaitez connaître les "
                                       "utilisateurs l'ayant utilisé"),
                     gr.Dataset(components=[gr.Textbox(visible=False)], label="Utilisateurs ayant utilisé le hashtag",
                                samples=[]),
                     live=True,
                     allow_flagging="never"
                     )

        btn.click(change_file_after_submitting, inputs=[f], outputs=[]) # On change le fichier après avoir cliqué sur le bouton "Envoyez"

    interface.launch(favicon_path="favicon.png")
