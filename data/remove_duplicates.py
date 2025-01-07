import pandas as pd

# Leer el archivo CSV en un DataFrame
df = pd.read_csv('raw_data_corpus.csv')  # Reemplaza 'archivo.csv' con el nombre de tu archivo CSV

# Eliminar filas duplicadas en base a la columna 'Title'
df_sin_duplicados = df.drop_duplicates(subset='Content', keep='first')

# Guardar el DataFrame sin duplicados en un nuevo archivo CSV
df_sin_duplicados.to_csv('archivo_sin_duplicados2.csv', index=False)

print("Se han eliminado las filas duplicadas y se ha guardado el archivo sin duplicados como 'archivo_sin_duplicados.csv'.")
