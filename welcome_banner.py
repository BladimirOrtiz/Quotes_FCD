import tkinter as tk
from tkinter import messagebox, PhotoImage, Entry, Label, Button
import webbrowser
import os
import login  # Importamos login.py para enlazarlo correctamente

def abrir_url(url):
    """ Abre enlaces en el navegador """
    webbrowser.open(url)

def crear_encabezado_footer(ventana):
    """ Crea el encabezado y footer con estilos unificados """

    # Encabezado
    header = tk.Frame(ventana, bg="#2E3B55", height=80)
    header.pack(fill="x")

    ruta_logo_izq = os.path.join("icono", "logofcd.png")
    ruta_logo_der = os.path.join("icono", "logo.png")

    try:
        logo_izquierdo = PhotoImage(file=ruta_logo_izq).subsample(5, 5)
        logo_derecho = PhotoImage(file=ruta_logo_der).subsample(5, 5)
    except:
        logo_izquierdo = None
        logo_derecho = None

    if logo_izquierdo:
        lbl_logo_izq = tk.Label(header, image=logo_izquierdo, bg="#2E3B55")
        lbl_logo_izq.image = logo_izquierdo
        lbl_logo_izq.pack(side="left", padx=10, pady=5)

    titulo = tk.Label(header, text="SISTEMA DE REGISTRO DE CITAS\n(FUNDACIÓN CORAZÓN DOWN)",
                      font=("Arial", 14, "bold"), bg="#2E3B55", fg="white")
    titulo.pack(side="left", expand=True)

    if logo_derecho:
        lbl_logo_der = tk.Label(header, image=logo_derecho, bg="#2E3B55")
        lbl_logo_der.image = logo_derecho
        lbl_logo_der.pack(side="right", padx=10, pady=5)

    # Footer
    footer = tk.Frame(ventana, bg="#D50000", height=120)
    footer.pack(side="bottom", fill="x")

    footer_content = tk.Frame(footer, bg="#D50000")
    footer_content.pack(fill="x")

    ruta_logo_footer = os.path.join("icono", "logofcd.png")

    try:
        logo_footer = PhotoImage(file=ruta_logo_footer).subsample(5, 5)
    except:
        logo_footer = None

    if logo_footer:
        lbl_logo_footer = tk.Label(footer_content, image=logo_footer, bg="#D50000")
        lbl_logo_footer.image = logo_footer
        lbl_logo_footer.pack(side="left", padx=20, pady=5)

    # Redes sociales
    info_frame = tk.Frame(footer_content, bg="#D50000")
    info_frame.pack(side="left", expand=True)

    redes_frame = tk.Frame(info_frame, bg="#D50000")
    redes_frame.pack()

    redes = {
        "Facebook": "ficon.png",
        "X": "xicon.png",
        "Instagram": "insicon.png",
        "TikTok": "ticon.png"
    }
    enlaces = {
        "Facebook": "https://www.facebook.com/FundacionCorazonDown",
        "X": "https://x.com/mariopmtz",
        "Instagram": "https://www.instagram.com/fundacioncorazondown",
        "TikTok": "https://www.tiktok.com/@corazndown"
    }

    for red, icono in redes.items():
        ruta_icono = os.path.join("icono", icono)
        try:
            img_red = PhotoImage(file=ruta_icono).subsample(2, 2)
            btn_red = tk.Button(redes_frame, image=img_red, bg="#D50000", relief="flat",
                                command=lambda u=enlaces[red]: abrir_url(u))
            btn_red.image = img_red
            btn_red.pack(side="left", padx=5)
        except:
            pass

    lbl_direccion = tk.Label(info_frame, text="XICOTÉNCATL 1017, ZONA FEB 10 2015, BARRIO DE LA NORIA, 68100 OAXACA DE JUÁREZ, OAX.",
                             font=("Arial", 9, "bold"), bg="#D50000", fg="white", wraplength=700, justify="center")
    lbl_direccion.pack(pady=(5, 0))

def ventana_welcome():
    """ Crea la pantalla principal de bienvenida """
    
    root = tk.Tk()
    root.title("Bienvenido - Fundación Corazón Down")

    # Ajustar la ventana al 80% de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.8)
    window_height = int(screen_height * 0.8)
    x_pos = (screen_width - window_width) // 2
    y_pos = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
    root.configure(bg="white")

    crear_encabezado_footer(root)

    tk.Label(root, text="BIENVENIDO/(A)", font=("Arial", 24, "bold"), bg="white", fg="#28A745").pack(pady=20)

    opciones_frame = tk.Frame(root, bg="white")
    opciones_frame.pack(fill="both", expand=True, pady=20)

    def abrir_login(rol):
        """Cierra la ventana actual y abre la de login sin crear miniventanas"""
        root.withdraw()  # Oculta la ventana principal sin cerrarla
        login.ventana_login_personalizada(rol, root)  # Pasa la ventana principal para restaurarla después

    botones = [
        ("administrador.png", "ADMINISTRADOR", "Administrador", "#E8F5E9", lambda: abrir_login("Administrador")),
        ("recepcion.png", "RECEPCIÓN", "Recepción", "#E3F2FD", lambda: abrir_login("Recepcionista")),
        ("terapeuta.png", "TERAPEUTA", "Terapeuta", "#FFEBEE", lambda: abrir_login("Terapeuta"))
    ]

    for i, (img, text, rol, color, command) in enumerate(botones):
        ruta_img = os.path.join("icono", img)
        try:
            img_btn = PhotoImage(file=ruta_img).subsample(3, 3)
        except:
            img_btn = None

        btn = tk.Button(opciones_frame, text=text, font=("Arial", 14, "bold"), bg=color, relief="flat", command=command)
        
        if img_btn:
            btn.config(image=img_btn, compound="top")
            btn.image = img_btn  # Evita garbage collector
        
        btn.grid(row=0, column=i, padx=15, pady=15, sticky="nsew")
        opciones_frame.columnconfigure(i, weight=1)

    root.mainloop()

if __name__ == "__main__":
    ventana_welcome()
