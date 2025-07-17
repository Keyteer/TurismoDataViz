import folium
import numpy as np
'''import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))'''

def generar_plot2(df, year=2020):
    world_geo = 'utils/countries.geo.json'
    map_arrivals = folium.Map(location=[20, 0], zoom_start=2, tiles='cartodb positron')

    # Calculate data range
    data_values = df[str(year)].dropna()
    min_val = data_values.min()
    max_val = data_values.max()

    # Generate more threshold points for smoother appearance
    threshold_scale = list(np.linspace(min_val, max_val, 60))

    folium.Choropleth(
        geo_data=world_geo,
        data=df,
        columns=['Country', str(year)],
        key_on='feature.properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f'Inbound Arrivals in {year}',
        threshold_scale=threshold_scale,
        nan_fill_color='#ffffff',
        legend_kwds={'spacing': '4000px'}
    ).add_to(map_arrivals)

    return map_arrivals

if __name__ == "__main__":
    from utils.cargarDataframes import load_arrivals_df
    df = load_arrivals_df()
    map_arrivals = generar_plot2(df, year=2020)
    #df.to_excel('df.xlsx', index=False)
    map_arrivals.save('plot2.html')
