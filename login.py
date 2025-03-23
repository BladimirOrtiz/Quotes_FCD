import tkinter as tk
from tkinter import messagebox, PhotoImage, Entry, Label, Button
import webbrowser
import os
import bcrypt
from conectar_bd import conectar_bd
import register  
import banner_admin
import banner_reception
import banner_therapeut 

def cerrar_aplicacion():
    """ Cierra la aplicación por completo """
    os._exit(0)  

def abrir_registro(ventana_login, rol):
    """ Cierra la ventana de login y abre la de registro con el rol correcto """
    ventana_login.destroy()
    register.ventana_registro(rol)

def recuperar_contraseña():
    """ Simula el proceso de recuperación de contraseña """
    messagebox.showinfo("Recuperación", "Proceso de recuperación de contraseña en desarrollo.")

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

def login(usuario, contraseña, rol, ventana_login, root):
    """Valida el login y redirige al banner correspondiente según el tipo de usuario."""
    conn = conectar_bd()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (usuario,))
    user = cursor.fetchone()

    conn.close()

    if user:
        stored_password = user["password"]
        stored_role = user["user_type"]

        if bcrypt.checkpw(contraseña.encode(), stored_password.encode()):
            if stored_role == rol:
                ventana_login.destroy()  # ✅ Cierra la ventana de login
                nueva_ventana = tk.Toplevel(root)  # ✅ Crea una nueva ventana para el panel
                root.withdraw()  # ✅ Oculta la ventana principal

                # ✅ Pasa correctamente `nueva_ventana` y `root` a cada banner
                if rol == "Administrador":
                    banner_admin.mostrar_panel_admin(nueva_ventana, root)
                elif rol == "Receptionist":
                    banner_reception.mostrar_panel_recepcion(nueva_ventana, root)
                elif rol == "Therapist":
                    banner_therapeut.mostrar_panel_terapeuta(nueva_ventana, root)
            else:
                messagebox.showerror("Error", f"El rol ingresado ({rol}) no coincide con el rol almacenado ({stored_role}).")
        else:
            messagebox.showerror("Error", "Contraseña incorrecta.")
    else:
        messagebox.showerror("Error", "El usuario no existe.")


def ventana_login_personalizada(rol, root):
    """Crea la ventana de login personalizada y oculta la aplicación principal."""
    ventana = tk.Toplevel(root)
    ventana.title(f"Login {rol} - Fundación Corazón Down")
    ventana.geometry("800x500")
    ventana.configure(bg="white")

    root.withdraw()  # ✅ Oculta `root` temporalmente

    crear_encabezado_footer(ventana)

    tk.Label(ventana, text=f"LOGIN {rol.upper()}", font=("Arial", 16, "bold"), bg="white", fg="black").pack(pady=10)

    entry_usuario = crear_entry(ventana, "Correo Electrónico")
    entry_password = crear_entry(ventana, "Contraseña", is_password=True)

    btn_login = Button(
        ventana, text="Iniciar Sesión",
        command=lambda: login(entry_usuario.get(), entry_password.get(), rol, ventana, root),
        font=("Arial", 12, "bold"), bg="red", fg="white", relief="flat", width=20, cursor="hand2"
    )
    btn_login.pack(pady=10)

    link_frame = tk.Frame(ventana, bg="white")
    link_frame.pack(pady=10)

    lbl_crear_cuenta = tk.Label(link_frame, text="Crear cuenta", font=("Arial", 10, "bold"), fg="orange", cursor="hand2", bg="white")
    lbl_crear_cuenta.pack(side="left", padx=10)
    lbl_crear_cuenta.bind("<Button-1>", lambda e: abrir_registro(ventana, rol))

    lbl_olvido_password = tk.Label(link_frame, text="Olvide mi contraseña", font=("Arial", 10, "bold"), fg="orange", cursor="hand2", bg="white")
    lbl_olvido_password.pack(side="left", padx=10)
    lbl_olvido_password.bind("<Button-1>", lambda e: recuperar_contraseña())

    ventana.protocol("WM_DELETE_WINDOW", lambda: root.deiconify())

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # ✅ Oculta la ventana principal al inicio
    ventana_login_personalizada("Administrador", root)
    root.mainloop()  # ✅ Mantiene la aplicación en ejecución
