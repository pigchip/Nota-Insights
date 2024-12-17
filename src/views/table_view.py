from customtkinter import *
from CTkTable import CTkTable

def setup_table_view(main_view,
                     title_text, 
                     entry_placeholder, 
                     button_text, 
                     global_results,
                     process_function, 
                     entry_label_text=None,
                     split_input=False):
    """
    Crea una vista genérica con:
    - Título
    - Campo de entrada (opcionalmente con un label)
    - Botón para disparar el proceso
    - Tabla para mostrar resultados
    """

    # Limpia la vista principal
    for widget in main_view.winfo_children():
        widget.destroy()

    # Título
    CTkLabel(master=main_view, text=title_text, font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", padx=20, pady=20)

    # Frame para campo de entrada
    input_frame = CTkFrame(master=main_view, fg_color="#F0F0F0")
    input_frame.pack(fill="x", padx=20, pady=10)

    # Campo de entrada (expandir horizontalmente)
    entry = CTkEntry(master=input_frame, placeholder_text=entry_placeholder)
    entry.pack(side="left", fill="x", expand=True, padx=10, pady=10)

    # Botón de acción (alineado a la derecha)
    CTkButton(master=input_frame, 
              text=button_text, 
              fg_color="#2A8C55", 
              text_color="#fff", 
              command=lambda: on_action_click(entry)
    ).pack(side="right", padx=10, pady=10)

    # Frame para la tabla
    table_frame = CTkScrollableFrame(master=main_view)
    table_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Función para mostrar resultados actuales en la tabla
    def render_table():
        for widget in table_frame.winfo_children():
            widget.destroy()

        if len(global_results) <= 1:
            CTkLabel(master=table_frame, 
                     text="No se encontraron resultados.", 
                     font=("Arial", 16), 
                     text_color="#555").pack(expand=True, pady=20)
        else:
            table = CTkTable(
                master=table_frame, 
                values=global_results, 
                colors=["#E6E6E6", "#EEEEEE"], 
                header_color="#2A8C55", 
                hover_color="#B4B4B4"
            )
            table.edit_row(0, text_color="#fff", hover_color="#2A8C55")
            table.pack(expand=True, fill="both")

    render_table()

    # Función de acción del botón
    def on_action_click(entry_widget):
        user_input = entry_widget.get().strip()
        entry_widget.delete(0, "end")

        global_results[:] = [global_results[0]]
        new_results = process_function(user_input.split() if split_input else user_input)

        if isinstance(new_results, list):
            global_results.extend(new_results)

        render_table()
