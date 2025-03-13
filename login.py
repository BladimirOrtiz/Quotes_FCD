import tkinter as tk
from tkinter import messagebox, PhotoImage, Entry, Label, Button
import webbrowser
import os
from conectar_bd import conectar_bd
import banner_admin
import banner_therapeut
import banner_reception

def abrir_url(url):
    webbrowser.open(url)

def crear_encabezado_footer(ventana):
    """Crea el encabezado y footer de la ventana con imágenes correctamente cargadas."""

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

def ventana_login_personalizada(rol, ventana_padre=None):
    ventana = tk.Toplevel()  # Ahora usamos Toplevel() para evitar miniventanas
    ventana.title(f"Login {rol} - Fundación Corazón Down")
    ventana.geometry("800x500")
    ventana.configure(bg="white")

    if ventana_padre:
        ventana.protocol("WM_DELETE_WINDOW", lambda: restaurar_ventana_principal(ventana, ventana_padre))

    crear_encabezado_footer(ventana)

    tk.Label(ventana, text=f"LOGIN {rol.upper()}", font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=10)

    # Entradas de usuario y contraseña
    entry_usuario = Entry(ventana, font=("Arial", 12))
    entry_usuario.pack(pady=5)
    entry_password = Entry(ventana, font=("Arial", 12), show="*")
    entry_password.pack(pady=5)

    btn_login = Button(ventana, text="INICIAR SESIÓN", font=("Arial", 12, "bold"), bg="red", fg="white", width=20)
    btn_login.pack(pady=20)

def restaurar_ventana_principal(ventana, ventana_padre):
    ventana.destroy()
    ventana_padre.deiconify()  # Restaura la ventana principal


def login(usuario, contraseña, rol):
    """Función para validar el login y abrir el menú principal."""
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (usuario, contraseña))
    user = cursor.fetchone()

    conn.close()

    if user:
        if user['user_type'] == rol:
            messagebox.showinfo("Bienvenido", f"Acceso concedido como {user['user_type']}")
            abrir_menu_principal(user)
        else:
            messagebox.showerror("Error", f"No tienes permisos de {rol}")
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")

def abrir_menu_principal(user):
    """Abre el menú principal dependiendo del tipo de usuario."""
    if user['user_type'] == 'Administrator':
        banner_admin(user)
    elif user['user_type'] == 'Receptionist':
        banner_reception(user)
    elif user['user_type'] == 'Therapist':
        banner_therapeut(user)

# Prueba de login (Opcional)
if __name__ == "__main__":
    ventana_login_personalizada("Administrador")
