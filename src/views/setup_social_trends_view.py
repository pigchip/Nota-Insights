from customtkinter import *
from modules.social_trends import get_trends_data

def setup_social_trends_view(main_view):
    """
    Configura la vista para mostrar tendencias en redes sociales con barras proporcionales y valores numéricos.
    """
    # Limpia la vista principal
    for widget in main_view.winfo_children():
        widget.destroy()

    # Título
    CTkLabel(master=main_view, text="Redes Sociales: Tendencias", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", padx=20, pady=20)

    # Frame para la tabla
    table_frame = CTkScrollableFrame(master=main_view)
    table_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Obtener los datos de tendencias
    trends = get_trends_data()  # [["Tendencia", Valor], ...]

    # Convertir los valores a float y ordenar por valor descendente
    for i in range(1, len(trends)):
        trends[i][1] = float(trends[i][1])
    trends[1:] = sorted(trends[1:], key=lambda x: x[1], reverse=True)

    # Crear tabla personalizada
    for i, row in enumerate(trends):
        if i == 0:  # Encabezado
            row_frame = CTkFrame(master=table_frame, fg_color="#2A8C55", corner_radius=10)
            row_frame.pack(fill="x", padx=5, pady=5)
            CTkLabel(master=row_frame, text=row[0], font=("Arial Bold", 12), text_color="white", width=150, anchor="w").pack(side="left", padx=10)
            CTkLabel(master=row_frame, text="Clasificación", font=("Arial Bold", 12), text_color="white", width=100, anchor="w").pack(side="right", padx=35)
            CTkLabel(master=row_frame, text="Valor", font=("Arial Bold", 12), text_color="white", width=120, anchor="e").pack(side="right", padx=35)
        else:
            value = row[1]
            label, color = get_popularity_label_and_color(value)
            normalized_value = value / 100.0

            # Contenedor de la fila
            row_frame = CTkFrame(master=table_frame, fg_color=color, corner_radius=10) 
            row_frame.pack(fill="x", padx=5, pady=5)

            # Sub-frame para nombre y barra, organizados en vertical
            info_frame = CTkFrame(master=row_frame, fg_color=color)
            info_frame.pack(side="left", fill="x", expand=True, padx=5, pady=5)

            # Nombre de la tendencia
            CTkLabel(master=info_frame, text=row[0], font=("Arial", 12), anchor="w", width=150).pack(anchor="w", padx=5)

            # Borde blanco alrededor de la barra
            border_frame = CTkFrame(master=info_frame, fg_color="white", corner_radius=10)
            border_frame.pack(anchor="w", padx=5, pady=5, fill="x")

            # Barra de progreso debajo del nombre
            progress_bar = CTkProgressBar(master=border_frame, height=20, progress_color=color, corner_radius=10)
            progress_bar.pack(fill="x", expand=True, padx=2, pady=2)
            progress_bar.set(normalized_value)

            # Valor numérico y etiqueta a la derecha
            CTkLabel(master=row_frame, text=f"{value:.2f}", font=("Arial", 12), width=80, anchor="w").pack(side="left", padx=10)
            CTkLabel(master=row_frame, text=label, font=("Arial", 12), width=120, anchor="w").pack(side="left", padx=10)

def get_popularity_label_and_color(value):
    """
    Devuelve una etiqueta descriptiva y un color de fondo/barra según el valor de mención.
    """
    if value >= 80:
        return "Altamente Popular", "#2A8C55"  # Verde oscuro
    elif value >= 65:
        return "Muy Popular", "#4CAF50"  # Verde intermedio oscuro
    elif value >= 50:
        return "Popular", "#A2C579"  # Verde medio
    elif value >= 35:
        return "Algo Popular", "#C8E6C9"  # Verde claro
    else:
        return "Poco Popular", "#E0E0E0"  # Gris claro
