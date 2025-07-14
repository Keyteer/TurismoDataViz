import numpy as np  # útil para cómputos matemáticos en Python
import pandas as pd  # biblioteca para estructuras de datos
import folium

url = 'https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/DV0101EN/labs/Data_Files/world_countries.json'
world_geo = '../utils/countries.geo.json'

map_arrivals = folium.Map(location=[20, 0], zoom_start=2, tiles='cartodb positron')

df = pd.read_excel('../Datasets/UN_Tourism_inbound_arrivals_11_2023.xlsx',
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



df = df[(df['Unnamed: 5'] == 'Total arrivals') | (df['Unnamed: 6'] == 'Overnights visitors (tourists)')]
df = df.drop(columns=['Unnamed: 4', 'Unnamed: 7'])

# change any '..' values to NaN
df = df.replace('..', np.nan)

# change countries from all caps to only first letter capitalized
df['Country'] = df['Country'].str.title()

# Read country mapping from CSV and apply it
mapping_df = pd.read_csv('../utils/country_mapping.csv')
df = df.merge(mapping_df, left_on='Country', right_on='original_name', how='left')
df['Country'] = df['geojson_name'].combine_first(df['Country'])
df = df.drop(['original_name', 'geojson_name'], axis=1)


# replace nan on totals with overnights values for every year and country
for year in df.columns[3:]:
    values = df[year].tolist()
    for i, value in enumerate(values):
        if pd.isna(values[i]) and i%2 == 0:
            values[i] = values[i+1]
    df[year] = values

df = df[df['Unnamed: 5'] == 'Total arrivals']

df = df.drop(columns=['Unnamed: 5', 'Unnamed: 6'])

df = df.reset_index(drop=True)

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

print(df)

df.to_excel('df.xlsx', index=False)

map_arrivals.save('map.html')
