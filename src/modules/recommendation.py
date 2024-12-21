# ============================================
# Función para Obtener Recomendaciones Basadas en Palabras Clave usando Sentence-BERT
# ============================================

def get_recommendation(keywords_list, top_n=5):
    """
    Genera recomendaciones de documentos basadas en una lista de palabras clave utilizando Sentence-BERT.
    
    Args:
        keywords_list (list): Lista de palabras clave para la búsqueda.
        top_n (int): Número de recomendaciones a retornar (por defecto: 5).
        
    Returns:
        list: Lista de listas con las recomendaciones.
              Formato: [["15: Impacto de la Economía", "0.95"], ...]
    """
    import os
    import pandas as pd
    import logging
    from sentence_transformers import SentenceTransformer, util
    import torch

    # ============================================
    # Configuración de Logging
    # ============================================
    logging.basicConfig(
        format='%(asctime)s : %(levelname)s : %(message)s',
        level=logging.INFO
    )

    # ============================================
    # Cargar Modelo de Sentence-BERT
    # ============================================
    try:
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')  # Modelo multilingüe eficiente
    except Exception as e:
        logging.error(f'Error al cargar el modelo de Sentence-BERT: {e}')
        return [["Error al cargar el modelo de Sentence-BERT.", ""]]

    # ============================================
    # Ruta al archivo CSV
    # ============================================
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, "../../data/raw_data_corpus.csv")

    # Leer el CSV
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
    except Exception as e:
        logging.error(f'Error al leer el archivo CSV: {e}')
        return [["Error al leer el archivo CSV.", ""]]

    # Verificar la existencia de las columnas necesarias
    if 'Content' not in df.columns or 'Title' not in df.columns:
        logging.error("El CSV debe contener las columnas 'Content' y 'Title'.")
        return [["Columnas 'Content' y/o 'Title' faltantes.", ""]]

    # ============================================
    # Obtener la lista de documentos y títulos
    # ============================================
    documentos = df['Content'].tolist()
    titulos = df['Title'].tolist()

    # ============================================
    # Obtener el índice original de los documentos en el CSV
    # ============================================
    # Sumamos 2 al índice para considerar la fila de encabezados (fila 1) y 1-based indexing
    filas = list(df.index + 2)  # Si el DataFrame index empieza en 0, fila CSV = index + 2

    # ============================================
    # Determinar Documentos Válidos
    # ============================================
    valid_docs_mask = []
    for doc, title in zip(documentos, titulos):
        # Verificar si 'Content' o 'Title' son NaN
        if pd.isna(doc) or pd.isna(title):
            valid_docs_mask.append(False)
            continue
        # Verificar si 'Content' o 'Title' contienen '&#160;'
        if '&#160;' in str(doc) or '&#160;' in str(title):
            valid_docs_mask.append(False)
            continue
        # Verificar si 'Content' o 'Title' son cadenas vacías o solo espacios en blanco
        if isinstance(doc, str):
            if doc.strip() == "":
                valid_docs_mask.append(False)
                continue
        else:
            # Si 'Content' no es una cadena, convertir a cadena y verificar
            if str(doc).strip() == "":
                valid_docs_mask.append(False)
                continue
        if isinstance(title, str):
            if title.strip() == "":
                valid_docs_mask.append(False)
                continue
        else:
            # Si 'Title' no es una cadena, convertir a cadena y verificar
            if str(title).strip() == "":
                valid_docs_mask.append(False)
                continue
        # Si pasa todas las validaciones, marcar como válido
        valid_docs_mask.append(True)

    # Obtener índices y datos de documentos válidos
    valid_indices = [i for i, valid in enumerate(valid_docs_mask) if valid]
    valid_documentos = [documentos[i] for i in valid_indices]
    valid_filas = [filas[i] for i in valid_indices]
    valid_titulos = [titulos[i] for i in valid_indices]

    if not valid_documentos:
        logging.error("No hay documentos válidos para procesar.")
        return [["No hay documentos válidos para procesar.", ""]]

    # ============================================
    # Generar embeddings para los documentos válidos
    # ============================================
    logging.info("Generando embeddings para los documentos válidos del corpus...")
    try:
        embeddings_corpus = model.encode(valid_documentos, convert_to_tensor=True, show_progress_bar=True)
    except Exception as e:
        logging.error(f'Error al generar embeddings para el corpus: {e}')
        return [["Error al generar embeddings para el corpus.", ""]]

    # ============================================
    # Verificar si la lista de palabras clave está vacía
    # ============================================
    if not keywords_list:
        logging.warning("La lista de palabras clave está vacía.")
        return [["No se proporcionaron palabras clave.", ""]]

    # ============================================
    # Preprocesar y generar embeddings para las palabras clave
    # ============================================
    query = ' '.join(keywords_list)
    logging.info("Generando embedding para las palabras clave...")
    try:
        embedding_query = model.encode(query, convert_to_tensor=True)
    except Exception as e:
        logging.error(f'Error al generar embedding para las palabras clave: {e}')
        return [["Error al generar embedding para las palabras clave.", ""]]

    # ============================================
    # Calcular similitudes de coseno
    # ============================================
    logging.info("Calculando similitudes...")
    try:
        cos_scores = util.cos_sim(embedding_query, embeddings_corpus)[0]
    except Exception as e:
        logging.error(f'Error al calcular similitudes: {e}')
        return [["Error al calcular similitudes.", ""]]

    # ============================================
    # Obtener los índices de los documentos con mayor similitud
    # ============================================
    top_results = torch.topk(cos_scores, k=top_n)

    # ============================================
    # Preparar las recomendaciones (sin encabezados)
    # ============================================
    recomendaciones = []
    for score, idx in zip(top_results[0], top_results[1]):
        fila = valid_filas[idx.item()]
        titulo = valid_titulos[idx.item()]
        fila_titulo = f"{fila}: {titulo}"
        similitud = round(score.item(), 4)  # Similaridad entre 0 y 1 con 4 decimales
        recomendaciones.append([fila_titulo, f"{similitud}"])

    return recomendaciones
