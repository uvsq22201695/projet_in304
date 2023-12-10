import plotly.graph_objects as go


def create_world_map(locations, countries, tweets):
    # make a map of the world
    fig = go.Figure(data=go.Choropleth(locations=countries,
                                       locationmode="ISO-3", z=tweets,
                                       text=locations,
                                       colorscale="Viridis", autocolorscale=False, reversescale=True,
                                       marker_line_color="darkgray",
                                       marker_line_width=0.5,
                                       colorbar_title="Nombre de tweets"))
    return fig
