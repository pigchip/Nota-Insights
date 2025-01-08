import pandas as pd

df = pd.read_csv('raw_data_corpus.csv')
df_sin_vacios = df[df['Content'].notna() & (df['Content'] != '')]
df_sin_vacios.to_csv('archivo_sin_vacios.csv', index=False)
print("Se han eliminado las filas con valores vacíos en la columna 'Content' y se ha guardado el archivo como 'archivo_sin_vacios.csv'.")
