from customtkinter import *
from modules.summarization import get_documents,summarize_document

def summarization_view(main_view):
    """
    Configura la vista para mostrar una lista de documentos seleccionables, un botón de resumen, y un área para mostrar el resumen del documento seleccionado.
    """
    # Limpia la vista principal
    for widget in main_view.winfo_children():
        widget.destroy()

    # Título
    CTkLabel(master=main_view, text="Documentos y Resumen", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", padx=20, pady=20)

    # Frame para el área de selección y resumen
    selection_frame = CTkFrame(master=main_view, fg_color="#F0F0F0", corner_radius=10)
    selection_frame.pack(side="top", fill="x", padx=20, pady=10)

    # Frame para el área de resumen
    summary_frame = CTkFrame(master=main_view, fg_color="#F0F0F0", corner_radius=10)
    summary_frame.pack(side="bottom", fill="both", padx=20, pady=20, expand=True)

    # Obtener los documentos (ejemplo de datos)
    documents = get_documents()  
    titles = documents['Title'].tolist()
    contents = documents['Content'].tolist()
    # Crear lista desplegable (select input) con scrollable dropdown
    selected_document = {"index": None}  # Para rastrear el documento seleccionado

    def select_document(event):
        """Actualiza el índice del documento seleccionado."""
        selected_document["index"] = dropdown_menu.get()

    # Crear menú desplegable con fondo blanco y scroll para manejar muchos documentos
    dropdown_menu = CTkOptionMenu(
        text_color="black",  # Cambiar texto a negro
        master=selection_frame,
        values= titles,  # Mostrar todos los documentos
        command=select_document,
        fg_color="white",  # Establecer fondo blanco
        button_color="#F0F0F0"
        #dropdown_height=200  # Limitar altura del menú desplegable con scroll
    )
    dropdown_menu.pack(side="left", padx=10, pady=10, fill="x", expand=True)

     # Botón para generar resumen
    def generate_summary():
        """Genera un resumen del documento seleccionado."""
        if selected_document["index"] is None:
            return  # No hay documento seleccionado

        # Buscar el índice del documento seleccionado
        index = titles.index(selected_document["index"])
        title = titles[index]
        content = contents[index]
        summary = summarize_document(content)  # Genera el resumen

        # Mostrar título y resumen
        for widget in summary_frame.winfo_children():
            widget.destroy()

        CTkLabel(master=summary_frame, text=f"Título: {title}", font=("Arial Black", 18), text_color="#2A8C55").pack(anchor="nw", padx=10, pady=10)
        CTkLabel(master=summary_frame, text=f"Resumen:\n{summary}", font=("Arial", 14), anchor="nw", justify="left", wraplength=600).pack(anchor="nw", padx=10, pady=10)

    CTkButton(
        master=selection_frame,
        text="Generar Resumen",
        command=generate_summary,
        fg_color="#2A8C55",
        text_color="white",
        corner_radius=10
    ).pack(side="right", padx=10, pady=10)


