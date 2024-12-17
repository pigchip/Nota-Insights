if __name__ == "__main__":
    import sys, os
    from customtkinter import *
    from CTkTable import CTkTable
    from PIL import Image

    from modules.search_engine import get_search_results
    from modules.recommendation import get_recommendation
    from modules.social_trends import *

    from views.table_view import setup_table_view
    from views.setup_plagiarism_view import setup_plagiarism_view
    from views.setup_social_trends_view import setup_social_trends_view

    def resource_path(relative_path):
        """Obtiene la ruta absoluta del recurso, ya sea empaquetado o no."""
        try:
            # PyInstaller crea una carpeta temporal para los archivos
            base_path = sys._MEIPASS
        except AttributeError:
            # En modo desarrollo, la ruta es relativa al directorio raíz del proyecto
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        return os.path.join(base_path, relative_path)

    set_appearance_mode("light")
    app = CTk()
    app.geometry("856x645")
    app.minsize(856, 645)
    app.resizable(True, True)
    app.title("Nota Insights")

    # Configurar ícono
    icon_path = resource_path("assets/images/logo.ico")
    try:
        app.iconbitmap(icon_path)
    except Exception as e:
        print(f"Error cargando el ícono: {e}")

    def clear_main_view():
        for widget in main_view.winfo_children():
            widget.destroy()

    # Definir una variable globales
    results = [["Documento", "Relevancia"]]
    recommendation_results = [["Artículo", "Relevancia"]]
    plagiarism_input = StringVar(value="")
    plagiarism_percentage = StringVar(value="0.00%")

    # Función auxiliar para configurar una vista con tabla y carga dinámica

    def show_search_engine():
        setup_table_view(
            main_view,
            title_text="Motor de Búsqueda",
            entry_placeholder="Escriba su consulta",
            button_text="Buscar",
            global_results=results,
            process_function=get_search_results,
            entry_label_text=None,
            split_input=False
        )

    def show_recommendation():
        setup_table_view(
            main_view,
            title_text="Recomendación de Contenido",
            entry_placeholder="Ej: tecnología economía...",
            button_text="Recomendar",
            global_results=recommendation_results,
            process_function=get_recommendation,
            entry_label_text="Palabras Clave:",
            split_input=True
        )

    def show_plagiarism():
        setup_plagiarism_view(
            main_view,
            plagiarism_input,
            plagiarism_percentage
        )
        
    def show_social_trends():
        setup_social_trends_view(main_view)

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
