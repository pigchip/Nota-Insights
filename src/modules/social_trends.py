import random
from PIL import Image

def get_trends_data():
    """
    Simula la obtención de 10 tendencias con valores aleatorios entre 1 y 100.
    """
    trends = [["Tendencia", "Mención"]]  # Encabezado de la tabla
    for i in range(1, 11):  # Generar 10 tendencias
        trends.append([f"#Tema{i}", str(random.randint(1, 100))])
    return trends

def load_chart_image(resource_path):
    """
    Carga la imagen de la gráfica.
    """
    try:
        chart_img_data = Image.open(resource_path)
        return chart_img_data
    except Exception:
        return None
