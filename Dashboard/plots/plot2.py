import numpy as np  # útil para cómputos matemáticos en Python
import pandas as pd  # biblioteca para estructuras de datos
import folium

url = 'https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files'
world_geo = f'{url}/world_countries.json'

map_arrivals = folium.Map(location=[20, 0], zoom_start=2, tiles='cartodb positron')

df = pd.read_excel('Datasets/UN_Tourism_inbound_arrivals_11_2023.xlsx',
                   sheet_name=' Inbound Tourism-Arrivals',
                   skiprows=2)

df = df.drop(columns=['C.', 'S.', 'C. & S.', 'Units', 'Notes', 'Series', 'Unnamed: 39'])
df = df.drop(range(1339,1346))

df = df.rename(columns={'Basic data and indicators': 'Country'})

# apply function to country column
country = None
country_list = df['Country'].tolist()
for i, x in enumerate(country_list):
    if pd.isna(x):
        country_list[i] = country
    else:
        country = x
df['Country'] = country_list



df = df[df['Unnamed: 5'] == 'Total arrivals']
df = df.drop(columns=['Unnamed: 4', 'Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7'])

# change any '..' values to NaN
df = df.replace('..', np.nan)

# change some country names to match the geojson file
df['Country'] = df['Country'].replace({
    'Czechia': 'Czech Republic',
    'UNITED STATES OF AMERICA': 'United States of America',
    'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
    'Republic of Korea': 'South Korea',
    'Viet Nam': 'Vietnam',
    'Bolivia (Plurinational State of)': 'Bolivia',
    'Iran (Islamic Republic of)': 'Iran',
    'Lao People\'s Democratic Republic': 'Laos',
    'Macao Special Administrative Region of China': 'Macao',
    'Venezuela, Bolivarian Republic Of': 'Venezuela',
})

# change countries from all caps to only first letter capitalized
df['Country'] = df['Country'].str.title()

# add 2020 arrivals to map Choropleth
folium.Choropleth(
    geo_data=world_geo,
    data=df,
    columns=['Country', 2020],
    key_on='feature.properties.name',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Inbound Arrivals in 2020'
).add_to(map_arrivals)

print(df.columns)

print(df)

map_arrivals.save('map.html')
