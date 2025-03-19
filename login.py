import tkinter as tk
from tkinter import messagebox, PhotoImage, Entry, Label, Button
import webbrowser
import os
from conectar_bd import conectar_bd
import register  # Importamos register.py para el registro de usuarios

# Importamos los banners correspondientes
import banner_admin
import banner_reception
import banner_therapeut 

def abrir_url(url):
    """ Abre enlaces en el navegador """
    webbrowser.open(url)

def cerrar_aplicacion():
    """ Cierra la aplicación por completo al cerrar una subventana. """
    os._exit(0)  # Termina la ejecución del programa

def abrir_registro(ventana_login, rol):
    """ Cierra la ventana de login y abre la de registro con el rol correcto """
    ventana_login.destroy()
    register.ventana_registro(rol)  # Abre la ventana de registro con el rol seleccionado

def recuperar_contraseña():
    """ Simula el proceso de recuperación de contraseña """
    messagebox.showinfo("Recuperación", "Proceso de recuperación de contraseña en desarrollo.")

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
    except Exception:
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

    lbl_direccion = tk.Label(footer_content, text="XICOTÉNCATL 1017, ZONA FEB 10 2015, BARRIO DE LA NORIA, 68100 OAXACA DE JUÁREZ, OAX.",
                             font=("Arial", 9, "bold"), bg="#D50000", fg="white", wraplength=700, justify="center")
    lbl_direccion.pack(pady=(5, 0))

def crear_entry(ventana, placeholder, is_password=False):
    """ Crea un campo de entrada estilizado con placeholder dinámico. """
    
    entry = Entry(ventana, font=("Arial", 12), fg="gray", relief="flat", width=40, bd=3)
    entry.insert(0, placeholder)
    
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, "end")
            entry.config(fg="black", show="*" if is_password else "")

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="gray", show="")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    entry.pack(pady=5, ipady=8, ipadx=5)
    entry.config(highlightthickness=2, highlightbackground="lightgray", highlightcolor="#28A745", relief="ridge")

    return entry

def login(usuario, contraseña, rol):
    """Valida el login y redirige al banner correspondiente según el tipo de usuario."""
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (usuario, contraseña))
    user = cursor.fetchone()

    conn.close()

    if user:
        if user['user_type'] == rol:
            messagebox.showinfo("Bienvenido", f"Acceso concedido como {user['user_type']}")
            
            # Redirigir según el rol del usuario
            if rol == "Administrator":
                banner_admin.mostrar_panel_admin()
            elif rol == "Receptionist":
                banner_reception.mostrar_panel_recepcion()
            elif rol == "Therapist":
                banner_therapeut.mostrar_panel_terapeuta()
        else:
            messagebox.showerror("Error", f"No tienes permisos de {rol}")
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")

def ventana_login_personalizada(rol, ventana_padre):
    """Crea la ventana de login personalizada y cierra la aplicación al cerrarla."""

    ventana = tk.Toplevel()  # Usamos Toplevel para evitar múltiples Tk()
    ventana.title(f"Login {rol} - Fundación Corazón Down")
    ventana.geometry("800x500")
    ventana.configure(bg="white")

    if ventana_padre:
        ventana_padre.withdraw()  # Oculta la ventana principal
        ventana.protocol("WM_DELETE_WINDOW", lambda: cerrar_aplicacion())  # Cierra la app al cerrar esta ventana

    crear_encabezado_footer(ventana)

    tk.Label(ventana, text=f"LOGIN {rol.upper()}", font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=10)

    # Entradas de usuario y contraseña
    entry_usuario = crear_entry(ventana, "Correo Electrónico")
    entry_password = crear_entry(ventana, "Contraseña", is_password=True)

    # Botón de login
    btn_login = Button(ventana, text="INICIAR SESIÓN", command=lambda: login(entry_usuario.get(), entry_password.get(), rol),
                       font=("Arial", 12, "bold"), bg="red", fg="white", relief="flat", width=20, cursor="hand2")
    btn_login.pack(pady=10)

    # Contenedor de hipervínculos
    link_frame = tk.Frame(ventana, bg="white")
    link_frame.pack(pady=10)

    lbl_crear_cuenta = tk.Label(link_frame, text="CREAR CUENTA", font=("Arial", 10, "bold"), fg="orange", cursor="hand2", bg="white")
    lbl_crear_cuenta.pack(side="left", padx=10)
    lbl_crear_cuenta.bind("<Button-1>", lambda e: abrir_registro(ventana, rol))

    lbl_olvido_password = tk.Label(link_frame, text="OLVIDÉ MI CONTRASEÑA", font=("Arial", 10, "bold"), fg="orange", cursor="hand2", bg="white")
    lbl_olvido_password.pack(side="left", padx=10)
    lbl_olvido_password.bind("<Button-1>", lambda e: recuperar_contraseña())

if __name__ == "__main__":
    root = tk.Tk()
    ventana_login_personalizada("Administrador", root)
