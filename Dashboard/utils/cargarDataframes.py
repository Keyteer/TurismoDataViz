import pandas as pd

def cargar_df1():
    # Cargar la hoja principal del Excel
    df1 = pd.read_excel("../Datasets/P_Data_Extract_From_World_Development_Indicators.xlsx", sheet_name="Data", engine="openpyxl")

    # Eliminar columnas completamente vacías
    df1 = df1.dropna(axis=1, how="all")

    # Eliminar filas completamente vacías (si las hay)
    df1 = df1.dropna(axis=0, how="all")

    return df1