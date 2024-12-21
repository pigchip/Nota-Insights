# ============================================
# 1. Importación de Bibliotecas Necesarias
# ============================================

import os
import pandas as pd
import logging
import numpy as np
from collections import defaultdict

# Bibliotecas de Procesamiento de Lenguaje Natural
import spacy
from nltk.corpus import stopwords
from gensim import corpora, models
from gensim.models import CoherenceModel
from gensim.models.phrases import Phrases, Phraser

# ============================================
# 2. Configuración de Logging
# ============================================

# Configurar logging para monitorear el proceso
logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO
)

# ============================================
# 3. Carga del Modelo de Lenguaje de spaCy
# ============================================

def cargar_modelo_spacy():
    """
    Carga el modelo de lenguaje en español de spaCy.
    Si el modelo no está instalado, se indica al usuario cómo instalarlo.
    """
    try:
        # Cargar el modelo en español, deshabilitando el parser y NER para mejorar el rendimiento
        nlp = spacy.load('es_core_news_sm', disable=['parser', 'ner'])
        return nlp
    except OSError:
        raise OSError(
            "El modelo 'es_core_news_sm' de spaCy no está instalado. "
            "Ejecuta 'python -m spacy download es_core_news_sm' para instalarlo."
        )

# Cargar el modelo de lenguaje
nlp = cargar_modelo_spacy()

# ============================================
# 4. Definición de Stopwords y Lista Blanca
# ============================================

# Stopwords adicionales en español para mejorar la eliminación de palabras comunes
custom_stopwords = {
    'casi', 'mucho', 'poco', 'tener', 'estar', 'ser', 'hacer', 'decir',
    'poder', 'ir', 'ver', 'dar', 'saber', 'querer', 'llegar', 'pasar', 'deber',
    'poner', 'parecer', 'quedar', 'creer', 'hablar', 'llevar', 'dejar', 'seguir',
    'encontrar', 'llamar', 'venir', 'pensar', 'salir', 'volver', 'tomar', 'conocer',
    'vivir', 'sentir', 'tratar', 'mirar', 'contar', 'empezar', 'esperar', 'buscar',
    'existir', 'entrar', 'trabajar', 'escribir', 'perder', 'producir', 'ocurrir',
    'entender', 'pedir', 'recibir', 'recordar', 'terminar', 'permitir', 'aparecer',
    'comenzar', 'servir', 'sacar', 'necesitar', 'mantener', 'resultar', 'leer',
    'caer', 'cambiar', 'presentar', 'crear', 'abrir', 'considerar', 'oír', 'acabar'
}

# Lista blanca de nombres propios y entidades que deben preservarse
whitelist = {
    'México', 'Brasil', 'Banco Central', 'Andrés', 'Manuel', 'López', 'Obrador',
    'ONU', 'FMI', 'UE', 'OMS', 'NASA', 'Apple', 'Microsoft'  # Añade más según tu corpus
}

# ============================================
# 5. Función de Preprocesamiento de Documentos
# ============================================

def preprocesar_documentos(documentos, stopwords_adicionales, whitelist, nlp):
    """
    Preprocesa los documentos aplicando tokenización, eliminación de stopwords,
    lematización, preservando nombres propios e instituciones, y filtrando por
    partes de la oración (sustantivos, nombres propios y adjetivos).
    
    Args:
        documentos (list): Lista de textos a procesar.
        stopwords_adicionales (set): Conjunto de stopwords adicionales.
        whitelist (set): Conjunto de palabras que deben preservarse.
        nlp (spaCy Language Model): Modelo de spaCy para procesamiento de texto.
        
    Returns:
        list: Lista de documentos preprocesados, cada uno como una lista de tokens.
    """
    # Combinar stopwords estándar con las adicionales
    stop_words = set(stopwords.words('spanish')).union(stopwords_adicionales)
    
    # Eliminar las palabras de whitelist de stopwords para preservarlas
    stop_words -= set([w.lower() for w in whitelist])
    
    documentos_procesados = []
    
    for doc in documentos:
        # Procesar el documento con spaCy
        spacy_doc = nlp(doc)
        lemmas = []
        for token in spacy_doc:
            if not token.is_alpha:
                continue  # Eliminar tokens no alfabéticos
            if token.pos_ not in {'NOUN', 'PROPN', 'ADJ'}:
                continue  # Incluir solo sustantivos, nombres propios y adjetivos
            lemma = token.lemma_.lower()
            if lemma in stop_words or lemma == 'nan':
                continue  # Eliminar stopwords y 'nan'
            if token.text in whitelist or token.pos_ == 'PROPN':
                lemmas.append(token.text)  # Preservar nombres propios e instituciones
            else:
                lemmas.append(lemma)  # Lematizar y convertir a minúsculas
            # Detectar palabras que se reducen a "nar"
            if lemma == 'nar':
                logging.warning(f'Palabra original: {token.text} fue transformada a "nar"')
        documentos_procesados.append(lemmas)
    
    return documentos_procesados

# ============================================
# 6. Función para Crear Bigrams
# ============================================

def crear_bigrams(documentos_procesados, min_count=3, threshold=50):
    """
    Crea bigrams para capturar nombres compuestos (como nombres de instituciones).
    
    Args:
        documentos_procesados (list): Lista de documentos preprocesados.
        min_count (int): Mínimo número de ocurrencias para formar un bigram.
        threshold (int): Umbral para determinar la formación de bigrams.
        
    Returns:
        list: Lista de documentos con bigrams aplicados.
    """
    bigram = Phrases(documentos_procesados, min_count=min_count, threshold=threshold)
    bigram_mod = Phraser(bigram)
    documentos_con_bigrams = [bigram_mod[doc] for doc in documentos_procesados]
    return documentos_con_bigrams

# ============================================
# 7. Función para Crear Diccionario y Corpus
# ============================================

def crear_diccionario_y_corpus(documentos, no_below=2, no_above=0.5):
    """
    Crea el diccionario y el corpus necesarios para el modelo LDA.
    
    Args:
        documentos (list): Lista de documentos con bigrams aplicados.
        no_below (int): Número mínimo de documentos en los que debe aparecer una palabra.
        no_above (float): Proporción máxima de documentos en los que puede aparecer una palabra.
        
    Returns:
        tuple: Diccionario de gensim y corpus (lista de bolsas de palabras).
    """
    # Crear diccionario (mapa palabra->id)
    dictionary = corpora.Dictionary(documentos)
    
    # Filtrar palabras muy raras o muy frecuentes
    dictionary.filter_extremes(no_below=no_below, no_above=no_above)
    
    # Convertir a corpus (lista de bolsas de palabras)
    corpus = [dictionary.doc2bow(doc) for doc in documentos]
    
    return dictionary, corpus

# ============================================
# 8. Función para Entrenar el Modelo LDA
# ============================================

def entrenar_modelo_lda(corpus, dictionary, num_topics=20, passes=20, iterations=400, alpha='auto', eta='auto'):
    """
    Entrena un modelo LDA utilizando LdaModel con un número fijo de temas.
    
    Args:
        corpus (list): Corpus en formato de bolsas de palabras.
        dictionary (gensim.corpora.Dictionary): Diccionario de gensim.
        num_topics (int): Número de temas a extraer.
        passes (int): Número de pasadas sobre el corpus durante el entrenamiento.
        iterations (int): Número de iteraciones por pasada.
        alpha (str): Parámetro alpha para LDA.
        eta (str): Parámetro eta para LDA.
        
    Returns:
        gensim.models.LdaModel: Modelo LDA entrenado.
    """
    lda_model = models.LdaModel(
        corpus=corpus,
        id2word=dictionary,
        num_topics=num_topics,
        passes=passes,
        iterations=iterations,
        alpha=alpha,
        eta=eta,
        random_state=42,
        eval_every=None,  # Desactivar evaluaciones intermedias
        per_word_topics=True
    )
    return lda_model

# ============================================
# 9. Función para Calcular la Coherencia del Modelo
# ============================================

def calcular_coherencia(lda_model, documentos_procesados, dictionary, coherence='c_v'):
    """
    Calcula la coherencia del modelo LDA.
    
    Args:
        lda_model (gensim.models.LdaModel): Modelo LDA entrenado.
        documentos_procesados (list): Lista de documentos preprocesados.
        dictionary (gensim.corpora.Dictionary): Diccionario de gensim.
        coherence (str): Tipo de coherencia a calcular.
        
    Returns:
        float: Puntaje de coherencia del modelo.
    """
    coherence_model = CoherenceModel(
        model=lda_model,
        texts=documentos_procesados,
        dictionary=dictionary,
        coherence=coherence
    )
    return coherence_model.get_coherence()

# ============================================
# 10. Función para Agregar Probabilidades de Temas Ponderadas
# ============================================

def agregar_probabilidades_temas(doc_topics, corpus, num_topics):
    """
    Agrega las probabilidades de los temas ponderadas por la longitud de los documentos.
    
    Args:
        doc_topics (list): Lista de distribuciones de temas por documento.
        corpus (list): Corpus en formato de bolsas de palabras.
        num_topics (int): Número total de temas.
        
    Returns:
        numpy.ndarray: Valores normalizados de temas ponderados.
    """
    topic_sums = defaultdict(float)
    for dt, doc_bow in zip(doc_topics, corpus):
        doc_length = sum([count for _, count in doc_bow])
        for topic_id, prob in dt:
            topic_sums[topic_id] += prob * doc_length
    
    # Convertir a array y normalizar
    topic_values = np.array([topic_sums[i] for i in range(num_topics)])
    max_val = topic_values.max()
    if max_val == 0:
        normalized_values = np.zeros(len(topic_values))
    else:
        normalized_values = (topic_values / max_val) * 100
    return normalized_values

# ============================================
# 11. Función para Extraer Tendencias del Modelo LDA
# ============================================

def extraer_tendencias(lda_model, topic_values, num_topics=20, topn=5):
    """
    Extrae las palabras más representativas de cada tema y las formatea para su presentación.
    
    Args:
        lda_model (gensim.models.LdaModel): Modelo LDA entrenado.
        topic_values (numpy.ndarray): Valores de temas ponderados y normalizados.
        num_topics (int): Número de temas.
        topn (int): Número de palabras principales por tema.
        
    Returns:
        list: Lista de listas con las tendencias y sus menciones.
              Formato: [["Tendencia", "Mención"], ["Tema 1", Valor1], ["Tema 2", Valor2], ...]
    """
    tendencias = [["Tendencia", "Mención"]]
    for i in range(num_topics):
        terms = lda_model.show_topic(i, topn=topn)
        # Filtrar y formatear palabras
        top_words = [
            w.capitalize() if not w.isupper() else w
            for w, _ in terms
            if w.lower() != 'nan'
        ]
        top_words = [w.replace('_', ' ') for w in top_words]
        topic_str = ", ".join(top_words)
        mention_value = round(topic_values[i], 2)
        tendencias.append([f"Tema {i+1}: {topic_str}", mention_value])
    return tendencias

# ============================================
# 12. Función Principal para Obtener Datos de Tendencias
# ============================================

def get_trends_data():
    """
    Lee el CSV, preprocesa el contenido, entrena un modelo LDA con 20 temas,
    y devuelve una lista de listas con las tendencias y sus valores basados
    en la frecuencia ponderada de los temas en el corpus.
    
    Returns:
        list: Lista de listas con las tendencias y sus menciones.
              Formato: [["Tendencia", "Mención"], ["Tema 1", Valor1], ["Tema 2", Valor2], ...]
    """
    # Ruta al archivo CSV
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, "../../data/raw_data_corpus.csv")
    
    # Leer el CSV
    try:
        df = pd.read_csv(csv_file, encoding='utf-8')
    except Exception as e:
        logging.error(f'Error al leer el archivo CSV: {e}')
        return [["Tendencia", "Mención"], ["Error al leer el archivo CSV", 0]]
    
    # Eliminar filas donde 'Content' es NaN
    df = df.dropna(subset=['Content'])
    
    # Verificar la existencia de la columna 'Content' y que no esté completamente vacía
    if 'Content' not in df.columns or df['Content'].isnull().all():
        logging.error("No hay datos válidos en la columna 'Content' después de eliminar NaNs.")
        return [["Tendencia", "Mención"], ["No hay datos válidos en 'Content'", 0]]
    
    # Obtener la lista de documentos
    documentos = df['Content'].astype(str).tolist()
    
    # Preprocesar documentos
    documentos_procesados = preprocesar_documentos(
        documentos,
        stopwords_adicionales=custom_stopwords,
        whitelist=whitelist,
        nlp=nlp
    )
    
    # Mostrar ejemplo de documentos preprocesados para verificar la integridad
    if documentos_procesados:
        logging.info("Ejemplo de documentos preprocesados:")
        for i in range(min(3, len(documentos_procesados))):
            logging.info(f'Doc {i+1}: {documentos_procesados[i][:10]}')  # Mostrar los primeros 10 tokens
    
    # Crear bigrams para capturar nombres compuestos
    documentos_con_bigrams = crear_bigrams(documentos_procesados)
    
    # Crear diccionario y corpus
    dictionary, corpus = crear_diccionario_y_corpus(documentos_con_bigrams)
    logging.info(f'Tamaño del diccionario después del filtrado: {len(dictionary)}')
    
    # Verificar datos suficientes para entrenar LDA
    if len(corpus) == 0 or len(dictionary) == 0:
        logging.error("No hay datos suficientes para entrenar LDA.")
        return [["Tendencia", "Mención"], ["No hay datos suficientes para entrenar LDA", 0]]
    
    # Entrenar el modelo LDA con 20 temas
    lda_model = entrenar_modelo_lda(corpus, dictionary, num_topics=20)
    
    # Calcular la coherencia del modelo
    coherencia = calcular_coherencia(lda_model, documentos_con_bigrams, dictionary, coherence='c_v')
    logging.info(f'Coherencia del modelo LDA con 20 temas: {coherencia:.4f}')
    
    # Obtener distribución de temas por documento
    doc_topics = [lda_model.get_document_topics(doc, minimum_probability=0.0) for doc in corpus]
    
    # Agregar las probabilidades ponderadas
    topic_values = agregar_probabilidades_temas(doc_topics, corpus, num_topics=20)
    
    # Extraer tendencias
    tendencias = extraer_tendencias(lda_model, topic_values, num_topics=20)
    
    return tendencias

# ============================================
# 13. Ejecución Principal
# ============================================

if __name__ == "__main__":
    tendencias = get_trends_data()
    if tendencias:
        print("Lista de Temas y sus Valores de Mención:\n")
        for tendencia in tendencias:
            print(f"{tendencia[0]}: {tendencia[1]}%")
    else:
        print("No se encontraron tendencias.")
