from customtkinter import *
from modules.plagiarism import process_plagiarism

def setup_plagiarism_view(main_view, 
                          plagiarism_input, 
                          plagiarism_percentage):
    """
    Configura la vista de análisis de plagio con un medidor visual de progreso.
    """
    # Limpia la vista principal
    for widget in main_view.winfo_children():
        widget.destroy()

    # Título
    CTkLabel(master=main_view, text="Análisis de Plagio", font=("Arial Black", 25), text_color="#2A8C55").pack(anchor="nw", padx=20, pady=20)

    # Frame de entrada
    input_frame = CTkFrame(master=main_view, fg_color="#F0F0F0")
    input_frame.pack(fill="x", padx=20, pady=10)

    # Caja de texto
    text_input = CTkTextbox(master=input_frame, height=200)
    text_input.insert("0.0", plagiarism_input.get())  # Cargar texto previo
    text_input.pack(fill="x", expand=True, padx=10, pady=10)

    # Botón de acción
    def analyze_plagiarism():
        new_input = text_input.get("0.0", "end").strip()
        new_percentage = process_plagiarism(new_input)

        try:
            progress_value = float(new_percentage.strip('%')) / 100
        except ValueError:
            progress_value = 0.0  # Asumir 0% si no es válido

        # Actualizar referencias globales
        plagiarism_input.set(new_input)
        plagiarism_percentage.set(new_percentage)

        # Actualizar progreso y resultado
        progress_bar.set(progress_value)
        progress_bar.configure(progress_color=get_color(progress_value))
        result_label.configure(text=f"Probabilidad de plagio: {float(progress_value * 100):.2f}%")

    CTkButton(master=input_frame, 
              text="Analizar", 
              fg_color="#2A8C55", 
              text_color="#fff",
              command=analyze_plagiarism).pack(pady=10)

    # Frame de resultados
    result_frame = CTkFrame(master=main_view, fg_color="#E6E6E6")
    result_frame.pack(fill="x", padx=20, pady=20)

    # Barra de progreso tipo medidor
    progress_bar = CTkProgressBar(master=result_frame, height=20, width=500)
    progress_bar.pack(padx=10, pady=10)
    progress_bar.set(0)  # Valor inicial en 0

    # Etiqueta de resultados
    result_label = CTkLabel(master=result_frame, 
                            text="Probabilidad de plagio: 0%", 
                            font=("Arial", 14), 
                            text_color="#333")
    result_label.pack(anchor="w", padx=10, pady=10)

    # Función para calcular el color basado en el progreso
    def get_color(progress):
        """
        Devuelve un color hexadecimal basado en el progreso.
        Verde (bajo) -> Rojo (alto)
        """
        r = int(255 * progress)  # Incrementa el rojo
        g = int(255 * (1 - progress))  # Decrementa el verde
        b = 0
        return f"#{r:02x}{g:02x}{b:02x}"  # Formato RGB a hexadecimal
