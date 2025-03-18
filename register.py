import tkinter as tk
from tkinter import messagebox, PhotoImage, Entry, Label, Button
import webbrowser
import os
from conectar_bd import conectar_bd
import login  # Importamos login.py para enlazar correctamente

def cerrar_aplicacion():
    """ Cierra la aplicación por completo al cerrar una subventana. """
    os._exit(0)  # Fuerza la terminación del programa sin dejar procesos abiertos

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
    except Exception as e:
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
    except Exception as e:
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
        except Exception as e:
            pass

    lbl_direccion = tk.Label(info_frame, text="XICOTÉNCATL 1017, ZONA FEB 10 2015, BARRIO DE LA NORIA, 68100 OAXACA DE JUÁREZ, OAX.",
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

def registrar_usuario(name, user_type, email, password):
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
        messagebox.showinfo("Éxito", "Usuario registrado correctamente")
        conn.close()
        cerrar_aplicacion()  # Cierra la app para reiniciar desde welcome_panel.py
    except Exception as e:
        messagebox.showerror("Error", f"Error al registrar: {str(e)}")
        conn.close()

def ventana_registro(rol):
    """ Crea la ventana de registro de usuario """
    ventana = tk.Toplevel()
    ventana.title("Registro de Usuario - Fundación Corazón Down")
    ventana.geometry("800x500")
    ventana.configure(bg="white")
    ventana.protocol("WM_DELETE_WINDOW", cerrar_aplicacion)
    
    crear_encabezado_footer(ventana)

    Label(ventana, text="REGISTRO DE USUARIO", font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=10)

    entry_nombre = crear_entry(ventana, "Nombre Completo")
    entry_email = crear_entry(ventana, "Correo Electrónico")
    entry_password = crear_entry(ventana, "Contraseña", is_password=True)

    # Dropdown de tipo de usuario
    opciones_roles = ["Administrator", "Receptionist", "Therapist"]
    user_type_var = tk.StringVar(ventana)
    user_type_var.set(opciones_roles[0])  # Valor por defecto
    menu_roles = tk.OptionMenu(ventana, user_type_var, *opciones_roles)
    menu_roles.config(font=("Arial", 12), bg="white", fg="black")
    menu_roles.pack(pady=10)

    # Botón de registro
    btn_registro = Button(ventana, text="REGISTRAR", command=lambda: registrar_usuario(entry_nombre.get(), user_type_var.get(), entry_email.get(), entry_password.get()),
                          font=("Arial", 12, "bold"), bg="red", fg="white", relief="flat", width=20, cursor="hand2")
    btn_registro.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    ventana_registro("Administrator")
