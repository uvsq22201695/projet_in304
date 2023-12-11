import plotly.graph_objects as go


def create_world_map(locations, countries, tweets):
    """
    Cette fonction permet de créer une carte du monde montrant le nombre de tweets par pays.
    :param locations: Liste des noms des pays
    :param countries: Liste des codes alpha_3 correspondants aux pays
    :param tweets: Liste de tweets
    :return fig: Carte du monde (Choropleth)
    """
    fig = go.Figure(data=go.Choropleth(locations=countries,
                                       locationmode="ISO-3", z=tweets,
                                       text=locations,
                                       colorscale="Viridis", autocolorscale=False, reversescale=True,
                                       marker_line_color="darkgray",
                                       marker_line_width=0.5,
                                       colorbar_title="Nombre de tweets"))
    return fig
