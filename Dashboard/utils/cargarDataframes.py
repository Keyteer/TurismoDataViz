import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)
'''import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))'''
from utils.traducirPais import traducir_pais

def df1(path = "Datasets/P_Data_Extract_From_World_Development_Indicators.xlsx"):
    # Cargar la hoja principal del Excel
    df1 = pd.read_excel(path, sheet_name="Data", engine="openpyxl")
    # Eliminar columnas completamente vacías
    df1 = df1.dropna(axis=1, how="all")
    # Eliminar filas completamente vacías (si las hay)
    df1 = df1.dropna(axis=0, how="all")
    # Eliminar fila Series Code
    df1 = df1.drop(columns=["Series Code"])
    # Transformar de formato ancho a largo
    df1_largo = df1.melt(
        id_vars=["Series Name", "Country Name", "Country Code"],
        var_name="Year",
        value_name="Value"
    )
    # Extraer solo el año numérico (ej: "1960 [YR1960]" → 1960)
    df1_largo["Year"] = df1_largo["Year"].str.extract(r"(\d{4})").astype(int)
    # Convertir valores a números reales
    df1_largo["Value"] = pd.to_numeric(df1_largo["Value"], errors="coerce")
    # Eliminar filas cuyo valor es NaN
    df1_largo = df1_largo.dropna(subset=["Value"])
    # Agregar traducción
    df1_largo["Nombre Español"] = df1_largo["Country Name"].apply(traducir_pais)
    # Ordenar segun nombre en español y año
    df1_largo = df1_largo.sort_values(by=["Nombre Español", "Year"]).reset_index(drop=True)
    return df1_largo

def load_arrivals_df(
    excel_path='Datasets/UN_Tourism_inbound_arrivals_11_2023.xlsx',
    mapping_path='utils/country_mapping.csv'
):
    df = pd.read_excel(
        excel_path,
        sheet_name=' Inbound Tourism-Arrivals',
        skiprows=2
    )
    df = df.drop(columns=['C.', 'S.', 'C. & S.', 'Units', 'Notes', 'Series', 'Unnamed: 39'])
    df = df.drop(range(1339,1346))
    df = df.rename(columns={'Basic data and indicators': 'Country'})

    # Fill missing country names
    country = None
    country_list = df['Country'].tolist()
    for i, x in enumerate(country_list):
        if pd.isna(x):
            country_list[i] = country
        else:
            country = x
    df['Country'] = country_list

    # Filter for arrivals and overnights
    df = df[(df['Unnamed: 5'] == 'Total arrivals') | (df['Unnamed: 6'] == 'Overnights visitors (tourists)')]
    df = df.drop(columns=['Unnamed: 4', 'Unnamed: 7'])

    # Replace '..' with NaN
    df = df.replace('..', np.nan)

    # Title case country names
    df['Country'] = df['Country'].str.title()

    # Map country names to geojson names
    mapping_df = pd.read_csv(mapping_path)
    df = df.merge(mapping_df, left_on='Country', right_on='original_name', how='left')
    df['Country'] = df['geojson_name'].combine_first(df['Country'])
    df = df.drop(['original_name', 'geojson_name'], axis=1)

    # Replace NaN in totals with overnights for each year/country
    df.columns = df.columns.astype(str).str.strip()
    for year in df.columns[3:]:
        values = df[year].tolist()
        for i, value in enumerate(values):
            if pd.isna(values[i]) and i % 2 == 0:
                values[i] = values[i+1]
        df[year] = values

    df = df[df['Unnamed: 5'] == 'Total arrivals']
    df = df.drop(columns=['Unnamed: 5', 'Unnamed: 6'])
    df = df.reset_index(drop=True)
    return df

if __name__ == "__main__":
    df = df1(path = "../Datasets/P_Data_Extract_From_World_Development_Indicators.xlsx")
    df_chile = df[df["Country Name"] == "Chile"]
    df_gdp_chile = df_chile[df_chile["Series Name"] == "International tourism, receipts (current US$)"]
    print(df_gdp_chile.head())
    arrivals_df = load_arrivals_df()
    print(arrivals_df.head())
