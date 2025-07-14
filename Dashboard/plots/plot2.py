import numpy as np
import pandas as pd
import os
import sys
import folium
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.cargarDataframes import load_arrivals_df

def generar_plot2(df, year=2020):
    """
    Generates a folium Choropleth map for inbound arrivals for a given year.
    Returns the folium Map object.
    """
    world_geo = '../utils/countries.geo.json'
    map_arrivals = folium.Map(location=[20, 0], zoom_start=2, tiles='cartodb positron')
    folium.Choropleth(
        geo_data=world_geo,
        data=df,
        columns=['Country', str(year)],
        key_on='feature.properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'Inbound Arrivals in {year}'
    ).add_to(map_arrivals)
    return map_arrivals

if __name__ == "__main__":
    df = load_arrivals_df()
    map_arrivals = generar_plot2(df, year=2020)
    print(df)
    df.to_excel('df.xlsx', index=False)
    map_arrivals.save('map.html')
