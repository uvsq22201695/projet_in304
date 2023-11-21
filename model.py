import gradio as gr

from entities import *
from histogram import *

RADIO_LABEL = "Top K"
RADIO_INFO = "Cochez la case si vous souhaitez avoir le top K renseignés."
RADIO_CHOICES = ["Hashtags", "Utilisateurs mentionnés", "Utilisateurs actifs", "Masquer"]
SLIDER_LABEL = "K "
SLIDER_INFO = "Veuillez choisir un nombre entre 2 et 50"

choices = {
    "Hashtags": "hashtags",
    "Utilisateurs actifs": "users",
    "Utilisateurs mentionnés": "users_mentioned",
}

THEME = "Base"


def make_model(tweets):
    """
    Cette fonction permet de créer l'interface graphique.
    :param tweets: Liste des tweets
    """

    entities_hashtags = count_entities(tweets, "hashtags")
    entities_users = count_entities(tweets, "users")
    entities_users_mentioned = count_entities(tweets, "arobase")

    temp = {
        "hashtags": entities_hashtags,
        "users": entities_users,
        "users_mentioned": entities_users_mentioned
    }

    # On crée l'interface graphique
    with (gr.Blocks(theme=THEME) as interface):

        def change_slider(choice: str, value: int):
            """
            Cette fonction permet d'afficher le slider et l'histogramme en fonction du choix de l'utilisateur.
            :param choice: Choix de l'utilisateur
            :param value: Valeur du slider
            :return: Slider et histogramme
            """

            current_val = value if value != 0 else 10  # On initialise la valeur du slider à 10 si elle est nulle

            # On vérifie si l'utilisateur a coché la case "Masquer"
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

            if username == "":
                return "# Veuillez entrer un nom d'utilisateur."

            value = entities_users.get(username)

            if value is None:
                return "# L'utilisateur **" + username + "** n'a pas publié."
            else:
                return "# L'utilisateur **" + username + "** a publié **" + str(value["occurence"]) + "** fois."

        def get_number_hashtag_publication(hashtag: str):
            """
            Cette fonction permet d'afficher le nombre de publications d'un hashtag.
            :param hashtag: Hashtag
            :return: Nombre de publications
            """

            if hashtag == "":
                return "# Veuillez entrer un hashtag."

            value = entities_hashtags.get(hashtag)

            if value is None:
                return "# Le hashtag **" + hashtag + "** n'a pas été utilisé."
            else:
                return "# Le hashtag **" + hashtag + "** a été utilisé **" + str(value["occurence"]) + "** fois."

        radio_top = gr.Radio(choices=RADIO_CHOICES, value="Masquer", label=RADIO_LABEL, info=RADIO_INFO)
        slider_hashtags = gr.Slider(visible=False)  # On crée le slider et on le cache
        plot_hashtags = gr.Plot(visible=False)  # On crée l'histogramme et on le cache

        # On regarde si une action a été effectuée sur le radio ou le slider
        radio_top.change(change_slider, inputs=[radio_top, slider_hashtags], outputs=[slider_hashtags, plot_hashtags])
        slider_hashtags.change(change_histogram, inputs=[radio_top, slider_hashtags], outputs=plot_hashtags)

        gr.Interface(get_number_user_publication,
                     [
                         gr.Textbox(label="Nombre de publications par un utilisateur",
                                    placeholder="Écrire le nom d'utilisateur ici", visible=True,
                                    max_lines=1, autoscroll=False),
                     ],
                     gr.Markdown("# Veuillez entrer un nom d'utilisateur."),
                     live=True
                     )

        gr.Interface(get_number_hashtag_publication,
                     [
                         gr.Textbox(label="Nombre de publications par hashtag",
                                    placeholder="Écrire le hashtag ici", visible=True,
                                    max_lines=1, autoscroll=False),
                     ],
                     gr.Markdown("# Veuillez entrer un hashtag."),
                     live=True
                     )

    interface.launch()
