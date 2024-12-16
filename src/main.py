import sys, os
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image

def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, ya sea empaquetado o no."""
    try:
        # PyInstaller crea una carpeta temporal para los archivos
        base_path = sys._MEIPASS
    except AttributeError:
        # En modo desarrollo (sin empaquetar), usar el directorio actual
        base_path = os.path.abspath("assets/images/")

    return os.path.join(base_path, relative_path)

set_appearance_mode("light")
app = CTk()

# Configurar ícono
icon_path = resource_path("assets/images/logo.ico")
try:
    app.iconbitmap(icon_path)
except Exception as e:
    print(f"Error cargando el ícono: {e}")

# Configurar la resolución inicial y mínima
app.geometry("856x645")  # Resolución inicial
app.minsize(856, 645)    # Resolución mínima
app.resizable(True, True)
app.title("Nota Insights")

def clear_main_view():
    for widget in main_view.winfo_children():
        widget.destroy()

def show_search_engine():
    clear_main_view()
    # Título
    CTkLabel(master=main_view, text="Motores de Búsqueda", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", padx=20, pady=20)

    # Campo de texto para la consulta
    query_frame = CTkFrame(master=main_view, fg_color="#F0F0F0")
    query_frame.pack(fill="x", padx=20, pady=10)
    query_entry = CTkEntry(master=query_frame, width=500, placeholder_text="Escriba su consulta")
    query_entry.pack(side="left", padx=10, pady=10)
    CTkButton(master=query_frame, text="Buscar", fg_color="#2A8C55", text_color="#fff").pack(side="left", padx=10)

    # Tabla de resultados (simulada)
    results = [
        ["Documento", "Relevancia"],
        ["Doc1", "0.95"],
        ["Doc2", "0.88"],
        ["Doc3", "0.80"]
    ]
    table_frame = CTkScrollableFrame(master=main_view)
    table_frame.pack(expand=True, fill="both", padx=20, pady=20)
    table = CTkTable(master=table_frame, values=results, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55", hover_color="#B4B4B4")
    table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
    table.pack(expand=True, fill="both")

def show_recommendation():
    clear_main_view()
    CTkLabel(master=main_view, text="Recomendación de Contenido", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", padx=20, pady=20)

    # Frame para selección de palabras clave
    keywords_frame = CTkFrame(master=main_view, fg_color="#F0F0F0")
    keywords_frame.pack(fill="x", padx=20, pady=10)
    CTkLabel(master=keywords_frame, text="Palabras Clave:", font=("Arial",14)).pack(side="left", padx=10, pady=10)
    keywords_entry = CTkEntry(master=keywords_frame, width=300, placeholder_text="Ej: 'tecnología', 'economía'...")
    keywords_entry.pack(side="left", padx=10, pady=10)
    CTkButton(master=keywords_frame, text="Recomendar", fg_color="#2A8C55", text_color="#fff").pack(side="left", padx=10)

    # Resultados de recomendación (simulados)
    results = [
        ["Artículo", "Relevancia"],
        ["Noticia A", "0.90"],
        ["Noticia B", "0.85"],
        ["Noticia C", "0.82"]
    ]
    table_frame = CTkScrollableFrame(master=main_view)
    table_frame.pack(expand=True, fill="both", padx=20, pady=20)
    table = CTkTable(master=table_frame, values=results, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55")
    table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
    table.pack(expand=True, fill="both")

def show_plagiarism():
    clear_main_view()
    CTkLabel(master=main_view, text="Análisis de Plagio", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", padx=20, pady=20)

    input_frame = CTkFrame(master=main_view, fg_color="#F0F0F0")
    input_frame.pack(fill="both", padx=20, pady=10, expand=False)
    text_input = CTkTextbox(master=input_frame, width=600, height=200)
    text_input.pack(side="left", padx=20, pady=20)

    CTkButton(master=input_frame, text="Analizar", fg_color="#2A8C55", text_color="#fff").pack(side="left", padx=20)

    result_frame = CTkFrame(master=main_view, fg_color="#E6E6E6", height=100)
    result_frame.pack(fill="x", padx=20, pady=20)
    CTkLabel(master=result_frame, text="Resultado:", font=("Arial Black", 15)).pack(anchor="w", padx=10, pady=(10,0))
    CTkLabel(master=result_frame, text="Probabilidad de plagio: 0.00%", font=("Arial",14), text_color="#333").pack(anchor="w", padx=10, pady=10)

def show_social_trends():
    clear_main_view()
    CTkLabel(master=main_view, text="Redes Sociales: Tendencias", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", padx=20, pady=20)

    # Simulación de gráficas
    chart_frame = CTkFrame(master=main_view, fg_color="#F0F0F0", height=300)
    chart_frame.pack(fill="x", padx=20, pady=20)
    try:
        chart_img_data = Image.open(resource_path("assets/images/chart.png"))
        chart_img = CTkImage(dark_image=chart_img_data, light_image=chart_img_data, size=(600,300))
        CTkLabel(master=chart_frame, text="", image=chart_img).pack(pady=10)
    except:
        CTkLabel(master=chart_frame, text="(Aquí se mostraría una gráfica de tendencias...)", font=("Arial",12)).pack(pady=10)

    # Lista de tendencias
    trends = [
        ["Tendencia", "Mención"],
        ["#Tema1", "5000"],
        ["#Tema2", "3200"],
        ["#Tema3", "2100"]
    ]
    table_frame = CTkScrollableFrame(master=main_view)
    table_frame.pack(expand=True, fill="both", padx=20, pady=20)
    table = CTkTable(master=table_frame, values=trends, colors=["#E6E6E6", "#EEEEEE"], header_color="#2A8C55")
    table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
    table.pack(expand=True, fill="both")

def show_summarization():
    clear_main_view()
    CTkLabel(master=main_view, text="Resumen Automático", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", padx=20, pady=20)

    # Simular documentos disponibles
    docs_frame = CTkFrame(master=main_view, fg_color="#F0F0F0")
    docs_frame.pack(fill="x", padx=20, pady=10)

    CTkLabel(master=docs_frame, text="Seleccione un documento:", font=("Arial",14)).pack(side="left", padx=10, pady=10)
    combo = CTkComboBox(master=docs_frame, values=["Documento 1", "Documento 2", "Documento 3"], button_color="#2A8C55", border_color="#2A8C55")
    combo.pack(side="left", padx=10, pady=10)

    CTkButton(master=docs_frame, text="Generar Resumen", fg_color="#2A8C55", text_color="#fff").pack(side="left", padx=10)

    # Mostrar el resumen generado
    result_frame = CTkFrame(master=main_view, fg_color="#E6E6E6")
    result_frame.pack(expand=True, fill="both", padx=20, pady=20)
    CTkLabel(master=result_frame, text="Resumen:", font=("Arial Black", 15)).pack(anchor="w", padx=10, pady=(10,0))
    CTkLabel(master=result_frame, text="Aquí se mostraría el resumen del documento seleccionado...", font=("Arial",14), text_color="#333", wraplength=600, justify="left").pack(anchor="w", padx=10, pady=10)

# SIDEBAR
sidebar_frame = CTkFrame(master=app, fg_color="#2A8C55", width=176, height=700, corner_radius=0)
sidebar_frame.pack_propagate(0)
sidebar_frame.pack(fill="y", anchor="w", side="left")

# Logo
logo_img_data = Image.open(resource_path("assets/images/logo.png"))
logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(150, 150))
CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

# Cargar imágenes para los botones
search_img_data = Image.open(resource_path("assets/images/search.png"))
like_img_data = Image.open(resource_path("assets/images/like.png"))
bug_img_data = Image.open(resource_path("assets/images/bug.png"))
bars_img_data = Image.open(resource_path("assets/images/bars.png"))
article_img_data = Image.open(resource_path("assets/images/article.png"))

search_img = CTkImage(dark_image=search_img_data, light_image=search_img_data)
like_img = CTkImage(dark_image=like_img_data, light_image=like_img_data)
bug_img = CTkImage(dark_image=bug_img_data, light_image=bug_img_data)
bars_img = CTkImage(dark_image=bars_img_data, light_image=bars_img_data)
article_img = CTkImage(dark_image=article_img_data, light_image=article_img_data)

CTkButton(master=sidebar_frame, image=search_img, text="Búsqueda", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=show_search_engine).pack(anchor="center", ipady=5, pady=(40, 0), fill="x")
CTkButton(master=sidebar_frame, image=like_img ,text="Recomendación", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=show_recommendation).pack(anchor="center", ipady=5, pady=(16, 0), fill="x")
CTkButton(master=sidebar_frame, image=bug_img , text="Plagio", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=show_plagiarism).pack(anchor="center", ipady=5, pady=(16, 0), fill="x")
CTkButton(master=sidebar_frame, image=bars_img , text="Tendencias", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=show_social_trends).pack(anchor="center", ipady=5, pady=(16, 0), fill="x")
CTkButton(master=sidebar_frame, image=article_img , text="Resumen", fg_color="transparent", font=("Arial Bold", 14), hover_color="#207244", anchor="w", command=show_summarization).pack(anchor="center", ipady=5, pady=(16, 0), fill="x")

# MAIN VIEW
main_view = CTkFrame(master=app, fg_color="#fff", width=924, height=700, corner_radius=0)
main_view.pack_propagate(0)
main_view.pack(side="left", fill="both", expand=True)

# Mostrar por defecto la primera sección
show_search_engine()

app.mainloop()
