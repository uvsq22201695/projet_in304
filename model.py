import gradio as gr
from histogram import *

def make_model(hashtags):
    with gr.Blocks(theme="Base") as interface:
        
        def change_slider(choice,previous_val):
            if "Hashtags" in choice:
                return {
                    slider_hashtags: gr.Slider(2, 50, value=previous_val if previous_val != 0 else 10, step=1, label="K hashtags",
                                  info=f"Veuillez choisir un nombre entre 2 et 50", visible=True, interactive=True),
                    plot_hashtags: gr.Plot(create_histogram_topk(topHashtags(previous_val, hashtags), "hashtags"), visible=True)
                }
            else:
                return {
                    slider_hashtags: gr.Slider(visible=False),
                    plot_hashtags: gr.Plot(visible=False)
                }
            
        def change_image(value):
            return {
                plot_hashtags: gr.Plot(create_histogram_topk(topHashtags(value, hashtags), "hashtags"), visible=True)
            }
        
        checkbox_top = gr.Checkboxgroup(["Hashtags"], label="Top K", info="Cochez la case si vous souhaitez avoir le top K renseignés.")
        
        slider_hashtags = gr.Slider(visible=False)
        plot_hashtags = gr.Plot(visible=False)
        
        checkbox_top.change(fn=change_slider, inputs=[checkbox_top, slider_hashtags], outputs=[slider_hashtags, plot_hashtags])
        slider_hashtags.change(fn=change_image, inputs=slider_hashtags, outputs=plot_hashtags)
    
    interface.launch()