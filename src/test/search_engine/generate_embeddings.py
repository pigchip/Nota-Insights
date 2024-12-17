import pandas as pd
import numpy as np
import torch
from transformers import BertTokenizer, BertModel
import os

MODEL_NAME = "dccuchile/bert-base-spanish-wwm-cased"

def get_bert_embedding(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()

if __name__ == '__main__':
    print("Cargando el modelo BETO...")
    tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
    model = BertModel.from_pretrained(MODEL_NAME)

    # Carpeta base del script actual
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Rutas relativas basadas en el script actual
    csv_file = os.path.join(script_dir, "../../../data/raw_data_corpus.csv")
    embeddings_file = os.path.join(script_dir, "../../embeddings/embeddings_corpus.npy")
    titles_file = os.path.join(script_dir, "../../../data/titles.csv")

    # Leer archivo CSV
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {csv_file}.")
        exit(1)

    print("Generando embeddings...")
    corpus = df["Content"].fillna("") + " " + df["Title"].fillna("")
    corpus_embeddings = [get_bert_embedding(text, tokenizer, model) for text in corpus]

    # Guardar archivos
    np.save(embeddings_file, corpus_embeddings)
    df[["Title"]].to_csv(titles_file, index=False)
    print("Embeddings y títulos guardados exitosamente!")
