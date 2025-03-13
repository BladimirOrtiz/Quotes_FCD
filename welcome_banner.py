import tkinter as tk
from tkinter import messagebox, PhotoImage
import webbrowser

def ventana_welcome():
    root = tk.Tk()
    root.title("Sistema de Registro de Citas - Fundación Corazón Down")

    # Obtiene resolución y ajusta tamaño de ventana al 80% de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = int(screen_width * 0.8)
    window_height = int(screen_height * 0.8)
    x_pos = (screen_width - window_width) // 2
    y_pos = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
    root.configure(bg="white")

    # Encabezado
    header = tk.Frame(root, bg="#2E3B55", height=80)
    header.pack(fill="x")

    logo_izquierdo = PhotoImage(file="icono/logofcd.png").subsample(5, 5)
    logo_derecho = PhotoImage(file="icono/logo.png").subsample(5, 5)

    lbl_logo_izq = tk.Label(header, image=logo_izquierdo, bg="#2E3B55")
    lbl_logo_izq.pack(side="left", padx=10, pady=5)

    titulo = tk.Label(header, text="SISTEMA DE REGISTRO DE CITAS\n(FUNDACIÓN CORAZÓN DOWN)",
                      font=("Arial", 14, "bold"), bg="#2E3B55", fg="white")
    titulo.pack(side="left", expand=True)

    lbl_logo_der = tk.Label(header, image=logo_derecho, bg="#2E3B55")
    lbl_logo_der.pack(side="right", padx=10, pady=5)

    lbl_bienvenido = tk.Label(root, text="BIENVENIDO/(A)", font=("Arial", 24, "bold"), bg="white", fg="#28A745")
    lbl_bienvenido.pack(pady=20)

    # Frame para los botones centrales
    opciones_frame = tk.Frame(root, bg="white")
    opciones_frame.pack(fill="both", expand=True, pady=20)

    # Cargar imágenes (puedes ajustar subsample dependiendo del tamaño de la pantalla)
    img_admin = PhotoImage(file="icono/administrador.png").subsample(3, 3)
    img_recepcion = PhotoImage(file="icono/recepcion.png").subsample(3, 3)
    img_terapeuta = PhotoImage(file="icono/terapeuta.png").subsample(3, 3)

    # Configurar grid dinámico
    for i, (img, text, rol, color) in enumerate([
        (img_admin, "ADMINISTRADOR", "Administrador", "#E8F5E9"),
        (img_recepcion, "RECEPCIÓN", "Recepción", "#E3F2FD"),
        (img_terapeuta, "TERAPEUTA", "Terapeuta", "#FFEBEE")
    ]):
        btn = tk.Button(opciones_frame, image=img, compound="top", text=text,
                        font=("Arial", 14, "bold"), bg=color, relief="flat", 
                        command=lambda r=rol: mensaje_bienvenida(r))
        btn.image = img  # Evita garbage collector
        btn.grid(row=0, column=i, padx=15, pady=15, sticky="nsew")
        opciones_frame.columnconfigure(i, weight=1)  # Todas las columnas crecen igual

    # Footer ajustable con redes sociales y dirección
    footer = tk.Frame(root, bg="#D50000")
    footer.pack(side="bottom", fill="x")

    footer_content = tk.Frame(footer, bg="#D50000")
    footer_content.pack(fill="x")

    logo_footer = PhotoImage(file="icono/logofcd.png").subsample(5, 5)
    lbl_logo_footer = tk.Label(footer_content, image=logo_footer, bg="#D50000")
    lbl_logo_footer.pack(side="left", padx=20, pady=5)

    # Redes sociales y dirección juntas
    info_frame = tk.Frame(footer_content, bg="#D50000")
    info_frame.pack(side="left", expand=True)

    redes_frame = tk.Frame(info_frame, bg="#D50000")
    redes_frame.pack()

    def abrir_url(url):
        webbrowser.open(url)

    # Cargar iconos de redes sociales (hacemos un poco más grandes)
    icono_facebook = PhotoImage(file="icono/ficon.png").subsample(2, 2)
    icono_x = PhotoImage(file="icono/xicon.png").subsample(2, 2)
    icono_instagram = PhotoImage(file="icono/insicon.png").subsample(2, 2)
    icono_tiktok = PhotoImage(file="icono/ticon.png").subsample(2, 2)

    for icono, url in [
        (icono_facebook, "https://www.facebook.com/FundacionCorazonDown"),
        (icono_x, "https://x.com/mariopmtz"),
        (icono_instagram, "https://www.instagram.com/fundacioncorazondown"),
        (icono_tiktok, "https://www.tiktok.com/@corazndown")
    ]:
        btn_red = tk.Button(redes_frame, image=icono, bg="#D50000", relief="flat", command=lambda u=url: abrir_url(u))
        btn_red.image = icono  # Evita garbage collector
        btn_red.pack(side="left", padx=5)

    lbl_direccion = tk.Label(info_frame, text="XICOTÉNCATL 1017, ZONA FEB 10 2015, BARRIO DE LA NORIA, 68100 OAXACA DE JUÁREZ, OAX.",
                             font=("Arial", 9, "bold"), bg="#D50000", fg="white", wraplength=window_width-50, justify="center")
    lbl_direccion.pack(pady=(5, 0))

    # Evitar que imágenes se eliminen
    root.logo_footer = logo_footer
    root.logo_izquierdo = logo_izquierdo
    root.logo_derecho = logo_derecho
    root.img_admin = img_admin
    root.img_recepcion = img_recepcion
    root.img_terapeuta = img_terapeuta
    root.icono_facebook = icono_facebook
    root.icono_x = icono_x
    root.icono_instagram = icono_instagram
    root.icono_tiktok = icono_tiktok

    root.mainloop()

def mensaje_bienvenida(rol):
    messagebox.showinfo("Bienvenido", f"Acceso como {rol}")

if __name__ == "__main__":
    ventana_welcome()
