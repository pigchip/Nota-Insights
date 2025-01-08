import pandas as pd

df = pd.read_csv('raw_data_corpus.csv')
df_sin_duplicados = df.drop_duplicates(subset='Content', keep='first')
df_sin_duplicados.to_csv('archivo_sin_duplicados2.csv', index=False)
print("Se han eliminado las filas duplicadas y se ha guardado el archivo sin duplicados como 'archivo_sin_duplicados.csv'.")
