import pandas as pd
import numpy as np
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import os

# Configuración del modelo BETO
MODEL_NAME = "dccuchile/bert-base-spanish-wwm-cased"

# Rutas relativas basadas en el script actual
script_dir = os.path.dirname(os.path.abspath(__file__))
embeddings_file = os.path.join(script_dir, "../embeddings/embeddings_corpus.npy")
titles_file = os.path.join(script_dir, "../../data/titles.csv")

# Cargar modelo y datos al importar
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertModel.from_pretrained(MODEL_NAME)
corpus_embeddings = np.load(embeddings_file, allow_pickle=True)
titles = pd.read_csv(titles_file)["Title"].tolist()

def get_bert_embedding(text, tokenizer, model):
    """Genera el embedding BERT para un texto dado."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).numpy()

def get_search_results(input_text):
    """
    Recibe un contenido de texto, calcula su similitud con los documentos existentes
    y devuelve los resultados en el formato especificado.
    """
    # Quitar espacios en blanco al principio y al final
    text = input_text.strip()
    if text == "":
        return []  # Devuelve una lista vacía si no hay entrada
    
    # Generar embedding para el texto de entrada
    query_embedding = get_bert_embedding(text, tokenizer, model)
    
    # Calcular similitud coseno con los embeddings del corpus
    similarities = [cosine_similarity(query_embedding, doc_emb)[0][0] for doc_emb in corpus_embeddings]
    
    # Ordenar los documentos por similitud descendente
    sorted_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)
    
    # Formatear resultados
    results = [
        [titles[i], f"{similarities[i]:.4f}"] 
        for i in sorted_indices[:3]  # Devolver solo los 3 mejores resultados
    ]
    return results
