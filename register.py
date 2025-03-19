import tkinter as tk
from tkinter import messagebox, PhotoImage, Entry, Label, Button, StringVar, OptionMenu
import webbrowser
import os
from conectar_bd import conectar_bd
import login  # Importamos login.py para enlazar correctamente

def cerrar_aplicacion():
    """ Cierra la aplicación por completo al cerrar una subventana. """
    os._exit(0)  # Termina la ejecución completamente

def abrir_url(url):
    """ Abre enlaces en el navegador """
    webbrowser.open(url)

def redirigir_login(rol, ventana_registro):
    """ Redirige al login con el rol correspondiente después del registro """
    messagebox.showinfo("Registro exitoso", "Usuario registrado correctamente. Redirigiendo al login...")
    ventana_registro.destroy()  # Cierra la ventana de registro
    login.ventana_login_personalizada(rol, None)  # Llama al login con el rol seleccionado

def registrar_usuario(name, user_type, email, password, rol, ventana_registro):
    """ Registra un nuevo usuario en la base de datos """
    if not name or not user_type or not email or not password:
        messagebox.showerror("Error", "Todos los campos son obligatorios")
        return
    
    conn = conectar_bd()
    cursor = conn.cursor()
    
    try:
        query = """
        INSERT INTO users (name, user_type, email, password) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (name, user_type, email, password))
        conn.commit()
        conn.close()
        redirigir_login(rol, ventana_registro)  # Redirige al login correspondiente
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar: {str(e)}")
        conn.close()

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

    ruta_logo_footer = os.path.join("icono", "logofcd.png")

    try:
        logo_footer = PhotoImage(file=ruta_logo_footer).subsample(5, 5)
    except Exception:
        logo_footer = None

    if logo_footer:
        lbl_logo_footer = tk.Label(footer_content, image=logo_footer, bg="#D50000")
        lbl_logo_footer.image = logo_footer
        lbl_logo_footer.pack(side="left", padx=20, pady=5)

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

def ventana_registro(rol):
    """ Crea la ventana de registro de usuario y termina el programa al cerrarla """
    ventana = tk.Toplevel()
    ventana.title(f"Registro de Usuario - {rol} - Fundación Corazón Down")
    ventana.geometry("800x500")
    ventana.configure(bg="white")

    # Si se cierra la ventana, se cierra toda la aplicación
    ventana.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)

    crear_encabezado_footer(ventana)

    Label(ventana, text=f"REGISTRO DE USUARIO - {rol.upper()}", font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=10)

    entry_nombre = crear_entry(ventana, "Nombre Completo")
    entry_email = crear_entry(ventana, "Correo Electrónico")
    entry_password = crear_entry(ventana, "Contraseña", is_password=True)

    # Traducción de roles en español y mapeo a inglés
    opciones_roles = {
        "Administrador": "Administrador",
        "Recepcionista": "Recercionista",
        "Terapeuta": "Terapeuta"
    }

    user_type_var = StringVar(ventana)
    user_type_var.set(rol)  # Se selecciona el rol pasado desde login.py

    # Menú desplegable deshabilitado (para evitar cambios de rol)
    menu_roles = OptionMenu(ventana, user_type_var, *opciones_roles.keys())
    menu_roles.config(font=("Arial", 12), bg="white", fg="black", state="disabled")  # No editable
    menu_roles.pack(pady=10)

    # Botón de registro
    btn_registro = Button(
        ventana, text="REGISTRAR",
        command=lambda: registrar_usuario(
            entry_nombre.get(), opciones_roles[rol], entry_email.get(), entry_password.get(), rol, ventana
        ),
        font=("Arial", 12, "bold"), bg="red", fg="white", relief="flat", width=20, cursor="hand2"
    )
    btn_registro.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal si se usa desde otro módulo
    ventana_registro("Administrador")
