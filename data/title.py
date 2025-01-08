import pandas as pd

df = pd.read_csv('raw_data_corpus.csv')
df_titles = df[['Title']]
df_titles.to_csv('titles.csv', index=False)

print("Se ha guardado la columna 'Title' en 'titulos.csv'.")
