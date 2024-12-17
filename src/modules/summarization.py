# src/modules/search_engine.py
import tkinter.messagebox as messagebox

def process_input(input_text):
    # Quitar espacios en blanco al principio y al final
    text = input_text.strip()
    if text == "":
        # Si la entrada está vacía, mostrar advertencia
        messagebox.showwarning("Advertencia", "La entrada está vacía. Por favor ingrese texto.")
        return ""
    else:
        # Devolver texto modificado
        return text + " MODIFICADA"
