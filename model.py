import gradio as gr

from entities import *
from histogram import *

RADIO_LABEL = "Top K"
RADIO_INFO = "Cochez la case si vous souhaitez avoir le top K renseignés."
RADIO_CHOICES = ["Hashtags", "Utilisateurs mentionnés", "Utilisateurs actifs"]
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
    with gr.Blocks(theme=THEME) as interface:

        def change_slider(choice: str, value: int):
            """
            Cette fonction permet d'afficher le slider et l'histogramme en fonction du choix de l'utilisateur.
            :param choice: Choix de l'utilisateur
            :param value: Valeur du slider
            :return: Slider et histogramme
            """

            current_val = value if value != 0 else 10  # On initialise la valeur du slider à 10 si elle est nulle

            # if choice:  # On vérifie si l'utilisateur à cocher la case
            return {
                    slider_hashtags: gr.Slider(2, 50, value=current_val, step=1,
                                               label=SLIDER_LABEL + choice.lower(),
                                               info=SLIDER_INFO, visible=True, interactive=True),
                    plot_hashtags: gr.Plot(create_histogram_top(topEntities(current_val, temp[choices[choice]]),
                                                                choices[choice]), visible=True)
                }
            # else:  # Si l'utilisateur n'a pas coché la case
            #     return {
            #         slider_hashtags: gr.Slider(visible=False),  # On cache le slider
            #         plot_hashtags: gr.Plot(visible=False)  # On cache l'histogramme
            #     }

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


        radio_top = gr.Radio(choices=RADIO_CHOICES, label=RADIO_LABEL, info=RADIO_INFO)  # On crée le radio
        slider_hashtags = gr.Slider(visible=False)  # On crée le slider et on le cache
        plot_hashtags = gr.Plot(visible=False)  # On crée l'histogramme et on le cache

        # On regarde si une action a été effectuée sur le radio ou le slider
        radio_top.change(change_slider, inputs=[radio_top, slider_hashtags], outputs=[slider_hashtags, plot_hashtags])
        slider_hashtags.change(change_histogram, inputs=[radio_top, slider_hashtags], outputs=plot_hashtags)

    interface.launch()
