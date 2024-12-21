import os
import pandas as pd
import logging
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def process_plagiarism(text_input):
    """
    Calcula el porcentaje de plagio utilizando BERT comparando el texto de entrada con un corpus de documentos.
    
    Args:
        text_input (str): Texto ingresado por el usuario.

    Returns:
        str: Porcentaje de plagio como un string formateado (Ej: "45.78%").
    """
    # Configuración de logging
    logging.basicConfig(level=logging.INFO)
    
    # ============================================
    # Definir Rutas
    # ============================================
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, "../../data/raw_data_corpus.csv")
    embeddings_dir = os.path.join(script_dir, "../embeddings")
    corpus_embeddings_path = os.path.join(embeddings_dir, "corpus_embeddings.npy")
    corpus_documents_path = os.path.join(embeddings_dir, "corpus_documents.npy")
    model_name = 'all-MiniLM-L6-v2'  # Puedes cambiar el modelo según tus necesidades
    
    # Crear el directorio de embeddings si no existe
    if not os.path.exists(embeddings_dir):
        try:
            os.makedirs(embeddings_dir)
            logging.info(f"Directorio de embeddings creado en: {embeddings_dir}")
        except Exception as e:
            logging.error(f"Error al crear el directorio de embeddings: {e}")
            return "Error al crear el directorio de embeddings."
    
    # ============================================
    # Cargar el Corpus
    # ============================================
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
        logging.info(f"Archivo CSV cargado correctamente desde: {csv_file}")
    except Exception as e:
        logging.error(f'Error al leer el archivo CSV: {e}')
        return "Error al leer el archivo CSV."
    
    # Verificar la existencia de las columnas necesarias
    if 'Content' not in df.columns or 'Title' not in df.columns:
        logging.error("El CSV debe contener las columnas 'Content' y 'Title'.")
        return "Columnas 'Content' y/o 'Title' faltantes."
    
    documentos = df['Content'].tolist()
    titulos = df['Title'].tolist()
    
    if not documentos:
        logging.error("El corpus está vacío.")
        return "El corpus está vacío."
    
    # ============================================
    # Cargar o Generar Embeddings del Corpus
    # ============================================
    if os.path.exists(corpus_embeddings_path) and os.path.exists(corpus_documents_path):
        try:
            corpus_embeddings = np.load(corpus_embeddings_path)
            corpus_documents = np.load(corpus_documents_path, allow_pickle=True).tolist()
            logging.info("Embeddings del corpus cargados desde archivos existentes.")
        except Exception as e:
            logging.error(f"Error al cargar los embeddings del corpus: {e}")
            return "Error al cargar los embeddings del corpus."
    else:
        # Cargar el Modelo de Sentence-Transformers
        try:
            model = SentenceTransformer(model_name)
            logging.info(f"Modelo '{model_name}' cargado correctamente.")
        except Exception as e:
            logging.error(f'Error al cargar el modelo de Sentence-Transformers: {e}')
            return "Error al cargar el modelo de procesamiento de texto."
        
        # Generar Embeddings para el Corpus
        try:
            logging.info("Generando embeddings para el corpus...")
            corpus_embeddings = model.encode(documentos, convert_to_tensor=False, show_progress_bar=True)
            corpus_documents = documentos  # Guardar los documentos para referencia futura
            logging.info("Embeddings generados correctamente.")
        except Exception as e:
            logging.error(f'Error al generar embeddings para el corpus: {e}')
            return "Error al procesar el corpus."
        
        # Guardar los Embeddings y Documentos
        try:
            np.save(corpus_embeddings_path, corpus_embeddings)
            np.save(corpus_documents_path, np.array(corpus_documents, dtype=object))
            logging.info(f"Embeddings y documentos del corpus guardados en: {embeddings_dir}")
        except Exception as e:
            logging.error(f"Error al guardar los embeddings del corpus: {e}")
            return "Error al guardar los embeddings del corpus."
    
    # ============================================
    # Cargar el Modelo (si no se cargó anteriormente)
    # ============================================
    if 'model' not in locals():
        try:
            model = SentenceTransformer(model_name)
            logging.info(f"Modelo '{model_name}' cargado correctamente para el texto de entrada.")
        except Exception as e:
            logging.error(f'Error al cargar el modelo de Sentence-Transformers: {e}')
            return "Error al cargar el modelo de procesamiento de texto."
    
    # ============================================
    # Procesar el Texto de Entrada
    # ============================================
    if not text_input.strip():
        return "0.00%"  # Si el texto está vacío, el porcentaje es 0.
    
    try:
        logging.info("Generando embedding para el texto de entrada...")
        input_embedding = model.encode([text_input], convert_to_tensor=False)[0]
        logging.info("Embedding del texto de entrada generado correctamente.")
    except Exception as e:
        logging.error(f'Error al generar el embedding del texto de entrada: {e}')
        return "Error al procesar el texto de entrada."
    
    # ============================================
    # Calcular Similitudes de Coseno
    # ============================================
    try:
        logging.info("Calculando similitudes de coseno...")
        similarities = cosine_similarity([input_embedding], corpus_embeddings)[0]
        logging.info("Similitudes calculadas correctamente.")
    except Exception as e:
        logging.error(f'Error al calcular similitudes: {e}')
        return "Error al calcular similitudes."
    
    if similarities.size == 0:
        logging.error("No se encontraron similitudes.")
        return "0.00%"
    
    # ============================================
    # Determinar el Porcentaje de Plagio
    # ============================================
    max_similarity = np.max(similarities)
    percentage = max_similarity * 100
    
    # Opcional: Aplicar un umbral para considerar solo similitudes relevantes
    threshold = 0.7  # Puedes ajustar este valor según tus necesidades
    if max_similarity < threshold:
        percentage = 0.0
    
    logging.info(f"Porcentaje de plagio calculado: {percentage:.2f}%")
    return f"{percentage:.2f}%"
