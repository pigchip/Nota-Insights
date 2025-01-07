import pandas as pd

# Leer el archivo CSV en un DataFrame
df = pd.read_csv('raw_data_corpus.csv')  # Reemplaza 'archivo.csv' con el nombre de tu archivo CSV

# Eliminar las filas donde la columna 'Content' tenga valores vacíos (NaN o cadena vacía)
df_sin_vacios = df[df['Content'].notna() & (df['Content'] != '')]

# Guardar el DataFrame sin las filas vacías en un nuevo archivo CSV
df_sin_vacios.to_csv('archivo_sin_vacios.csv', index=False)

print("Se han eliminado las filas con valores vacíos en la columna 'Content' y se ha guardado el archivo como 'archivo_sin_vacios.csv'.")
