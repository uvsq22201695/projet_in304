import gradio as gr

from entities import *
from histogram import *


def make_model(tweets):
    with gr.Blocks(theme="Base") as interface:

        def change_slider(choice, previous_val):
            current_val = previous_val if previous_val != 0 else 10
            histo = create_histogram_topk(topEntities(current_val, count_entities(tweets, choice.lower())),
                                          choice.lower())
            if choice:
                return {
                    slider_hashtags: gr.Slider(2, 50, value=current_val, step=1, label=f"K {choice.lower()}",
                                               info=f"Veuillez choisir un nombre entre 2 et 50", visible=True,
                                               interactive=True),
                    plot_hashtags: gr.Plot(histo, visible=True)
                }
            else:
                return {
                    slider_hashtags: gr.Slider(visible=False),
                    plot_hashtags: gr.Plot(visible=False)
                }

        def change_histogram(choice, value):
            histo = create_histogram_topk(topEntities(value, count_entities(tweets, choice.lower())), choice.lower())
            return {
                plot_hashtags: gr.Plot(histo, visible=True)
            }

        radio_top = gr.Radio(["Hashtags", "Arobases", "Users"], label="Top K",
                             info="Cochez la case si vous souhaitez avoir le top K renseignés.")

        slider_hashtags = gr.Slider(visible=False)
        plot_hashtags = gr.Plot(visible=False)

        radio_top.change(fn=change_slider, inputs=[radio_top, slider_hashtags],
                         outputs=[slider_hashtags, plot_hashtags])
        slider_hashtags.change(fn=change_histogram, inputs=[radio_top, slider_hashtags], outputs=plot_hashtags)

    interface.launch()
