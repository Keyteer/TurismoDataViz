import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)


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

    return df1_largo

if __name__ == "__main__":
    df = df1(path = "../Datasets/P_Data_Extract_From_World_Development_Indicators.xlsx")
    df_chile = df[df["Country Name"] == "Chile"]
    df_gdp_chile = df_chile[df_chile["Series Name"] == "International tourism, receipts (current US$)"]
    print(df_gdp_chile.head())