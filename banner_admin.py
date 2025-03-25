import tkinter as tk
from tkinter import Button, Label, PhotoImage, Frame
import webbrowser
import os
import login  # Para cerrar sesión y volver al login
from quotes_register import ventana_registro_cita  # ✅ Importar al inicio

def cerrar_sesion(ventana, root):
    ventana.destroy()
    root.deiconify()
    login.ventana_login_personalizada("Administrador", root)

def abrir_url(url):
    webbrowser.open(url)

def mostrar_panel_admin(ventana, root):
    ventana.title("Panel Administrador - Fundación Corazón Down")
    ventana.geometry("960x540")
    ventana.configure(bg="white")

    # ───── ENCABEZADO ─────
    header = tk.Frame(ventana, bg="#2E3B55", height=80)
    header.pack(fill="x")

    try:
        logo_izquierdo = PhotoImage(file="icono/logofcd.png").subsample(5, 5)
        logo_derecho = PhotoImage(file="icono/logo.png").subsample(5, 5)
    except:
        logo_izquierdo = logo_derecho = None

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

    # ───── CONTENEDOR PRINCIPAL ─────
    frame_principal = tk.Frame(ventana, bg="white")
    frame_principal.pack(expand=True, fill="both", pady=20)

    botones = [
        ("icono/calendario.png", "REGISTRO DE CITAS", "#FF9800", ventana_registro_cita),
        ("icono/gestion.png", "GESTIÓN DE CITAS", "#3F51B5", lambda: print("Gestión de citas")),
        ("icono/estadisticas.png", "ESTADÍSTICAS", "#4CAF50", lambda: print("Estadísticas"))
    ]

    for i, (img_path, text, color, command) in enumerate(botones):
        try:
            img = PhotoImage(file=img_path).subsample(4, 4)
        except:
            img = None

        btn = Button(
            frame_principal,
            text=text,
            font=("Arial", 13, "bold"),
            bg=color,
            fg="white",
            relief="flat",
            width=180,
            height=120,
            command=command,
            compound="top",
            padx=10,
            pady=10
        )

        if img:
            btn.config(image=img)
            btn.image = img

        btn.grid(row=0, column=i, padx=30, pady=20, sticky="nsew")
        frame_principal.columnconfigure(i, weight=1)

    # ───── FOOTER COMPLETO ─────
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

    lbl_direccion = tk.Label(
        info_frame,
        text="XICOTÉNCATL 1017, ZONA FEB 10 2015, BARRIO DE LA NORIA, 68100 OAXACA DE JUÁREZ, OAX.",
        font=("Arial", 9, "bold"), bg="#D50000", fg="white",
        wraplength=700, justify="center"
    )
    lbl_direccion.pack(pady=(5, 0))

    # Botón de cerrar sesión
    btn_cerrar_sesion = Button(
        ventana, text="CERRAR SESIÓN", font=("Arial", 12, "bold"),
        bg="red", fg="white", relief="flat", width=20, cursor="hand2",
        command=lambda: cerrar_sesion(ventana, root)
    )
    btn_cerrar_sesion.pack(pady=10)

    ventana.mainloop()
