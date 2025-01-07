import pandas as pd

# Leer el archivo CSV en un DataFrame
df = pd.read_csv('raw_data_corpus.csv')  # Reemplaza 'archivo.csv' con el nombre de tu archivo CSV

# Extraer solo la columna 'Title'
df_titles = df[['Title']]

# Guardar la columna 'Title' en un nuevo archivo CSV
df_titles.to_csv('titles.csv', index=False)

print("Se ha guardado la columna 'Title' en 'titulos.csv'.")
