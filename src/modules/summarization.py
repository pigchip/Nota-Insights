# src/modules/search_engine.py
import tkinter.messagebox as messagebox
import pandas as pd
import os
import logging    
import torch
from transformers import BartTokenizer, BartForConditionalGeneration
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import evaluate
import nltk
nltk.download('punkt_tab')

# Cargar la métrica ROUGE
rouge = evaluate.load("rouge")

# Configuración del modelo BART
MODEL_NAME = "facebook/bart-large-cnn"  # Modelo preentrenado para resúmenes
tokenizer = BartTokenizer.from_pretrained(MODEL_NAME)
model = BartForConditionalGeneration.from_pretrained(MODEL_NAME)

def summarize_document(input_text, max_length=100, min_length=20):
    # Tokenizar el texto de entrada
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, max_length=1024)

    # Generar el resumen con el modelo BART
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=max_length,
        min_length=min_length,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True
    )

    # Decodificar el resumen generado
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
    evaluate_with_rouge(input_text,summary)
    return summary
    
# Función para evaluar el resumen con ROUGE
def evaluate_with_rouge(original_text, generated_summary):
    
    
    results = rouge.compute(predictions=[generated_summary], references=[original_text])

    # Mostrar resultados
    print("Resultados de ROUGE:")
    # Manejo según la estructura de los resultados
    for key, value in results.items():
        if isinstance(value, dict):  # Verifica si el resultado es un diccionario
            print(f"{key}:")
            print(f"  Precisión: {value['precision']:.4f}")
            print(f"  Recuperación: {value['recall']:.4f}")
            print(f"  F1-Score: {value['fmeasure']:.4f}")
        else:
            print(f"{key}: {value:.4f}")  # Si el resultado es escalar
    return results

def get_documents():
    # ============================================
    # Ruta al archivo CSV
    # ============================================
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, "../../data/raw_data_corpus.csv")
    # ============================================
    # Leer el CSV
    # ============================================
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
        logging.info(f"Archivo CSV cargado correctamente desde: {csv_file}")
    except Exception as e:
        logging.error(f'Error al leer el archivo CSV: {e}')
        return [["Error al leer el archivo CSV.", ""]]
    data = df[['Title','Content']]
    print(data)
    return data
    