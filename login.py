import tkinter as tk
from tkinter import messagebox, PhotoImage, Entry, Label, Button
import webbrowser
from conectar_bd import conectar_bd
import banner_admin
import banner_therapeut
import banner_reception

def abrir_url(url):
    webbrowser.open(url)

def crear_encabezado_footer(ventana):
    # Encabezado
    header = tk.Frame(ventana, bg="#2E3B55", height=80)
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

    ventana.logo_izquierdo = logo_izquierdo
    ventana.logo_derecho = logo_derecho

    # Footer
    footer = tk.Frame(ventana, bg="#D50000", height=120)
    footer.pack(side="bottom", fill="x")

    footer_content = tk.Frame(footer, bg="#D50000")
    footer_content.pack(fill="x")

    logo_footer = PhotoImage(file="icono/logofcd.png").subsample(5, 5)
    lbl_logo_footer = tk.Label(footer_content, image=logo_footer, bg="#D50000")
    lbl_logo_footer.pack(side="left", padx=20, pady=5)

    info_frame = tk.Frame(footer_content, bg="#D50000")
    info_frame.pack(side="left", expand=True)

    redes_frame = tk.Frame(info_frame, bg="#D50000")
    redes_frame.pack()

    # Iconos de redes sociales
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
        btn_red.image = icono
        btn_red.pack(side="left", padx=5)

    lbl_direccion = tk.Label(info_frame, text="XICOTÉNCATL 1017, ZONA FEB 10 2015, BARRIO DE LA NORIA, 68100 OAXACA DE JUÁREZ, OAX.",
                             font=("Arial", 9, "bold"), bg="#D50000", fg="white", wraplength=700, justify="center")
    lbl_direccion.pack(pady=(5, 0))

    ventana.logo_footer = logo_footer
    ventana.icono_facebook = icono_facebook
    ventana.icono_x = icono_x
    ventana.icono_instagram = icono_instagram
    ventana.icono_tiktok = icono_tiktok

def ventana_login_personalizada(rol):
    ventana = tk.Tk()
    ventana.title(f"Login {rol} - Fundación Corazón Down")
    ventana.geometry("800x500")
    ventana.configure(bg="white")

    crear_encabezado_footer(ventana)

    tk.Label(ventana, text=f"LOGIN {rol.upper()}", font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=10)

    # Icono de usuario
    icono_usuario = PhotoImage(file="icono/user.png").subsample(3, 3)
    lbl_icono = tk.Label(ventana, image=icono_usuario, bg="white")
    lbl_icono.pack(pady=10)

    # Entradas de usuario y contraseña
    entry_usuario = Entry(ventana, font=("Arial", 12), fg="green", relief="flat", width=40)
    entry_usuario.insert(0, "USUARIO")
    entry_usuario.pack(pady=5)

    entry_password = Entry(ventana, font=("Arial", 12), show="*", fg="green", relief="flat", width=40)
    entry_password.insert(0, "CONTRASEÑA")
    entry_password.pack(pady=5)

    # Botón de login
    btn_login = Button(ventana, text="INICIAR SESIÓN", command=lambda: login(entry_usuario.get(), entry_password.get(), rol),
                       font=("Arial", 12, "bold"), bg="red", fg="white", relief="flat", width=20)
    btn_login.pack(pady=20)

    # Evitar recolección de basura
    ventana.icono_usuario = icono_usuario

    ventana.mainloop()

def login(usuario, contraseña, rol):
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
    if user['user_type'] == 'Administrator':
        banner_admin(user)
    elif user['user_type'] == 'Receptionist':
        banner_reception(user)
    elif user['user_type'] == 'Therapist':
        banner_therapeut(user)

# Ejemplo de cómo lanzar la ventana personalizada
if __name__ == "__main__":
    ventana_login_personalizada("Administrador")
