def get_search_results(input_text):
    # Quitar espacios en blanco al principio y al final
    text = input_text.strip()
    if text == "":
        return []  # Devuelve una lista vacía si no hay entrada
    else:
        # Simulación de resultados de búsqueda
        return [
            ["Documento 1", f"{text} - Resultado 1"],
            ["Documento 2", f"{text} - Resultado 2"],
            ["Documento 3", f"{text} - Resultado 3"]
        ]
