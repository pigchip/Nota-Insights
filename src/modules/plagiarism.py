import random

def process_plagiarism(text_input):
    """
    Simula el procesamiento del texto para calcular un porcentaje de plagio.
    
    Args:
        text_input (str): Texto ingresado por el usuario.

    Returns:
        str: Porcentaje de plagio como un string formateado (Ej: "45.78%").
    """
    if not text_input.strip():
        return "0.00%"  # Si el texto está vacío, el porcentaje es 0.

    # Simula un procesamiento más complejo aquí
    percentage = random.uniform(0, 100)
    return f"{percentage:.2f}%"
