def get_recommendation(keywords_list):
    """
    Simula una lógica de recomendación basada en una lista de palabras clave.
    """
    # Validar si la lista de palabras clave está vacía
    if not keywords_list:
        return []

    # Simular recomendaciones generadas por cada palabra clave
    recommendations = []

    for i, keyword in enumerate(keywords_list):
        # Ejemplo: Crear resultados basados en cada palabra clave
        recommendations.append([f"Artículo relacionado con '{keyword}'", f"{0.9 - i*0.05:.2f}"])

    return recommendations
