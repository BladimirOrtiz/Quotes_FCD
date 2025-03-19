import tkinter as tk
from tkinter import PhotoImage, Button, Label
import os
import login  # Para cerrar sesión y volver al login
import register  # Si es necesario registrar nuevos usuarios

# Funciones para abrir módulos correspondientes
def abrir_registro_citas():
    """Función para abrir el módulo de registro de citas"""
    print("Abriendo módulo de Registro de Citas...")

def abrir_gestion_citas():
    """Función para abrir el módulo de gestión de citas"""
    print("Abriendo módulo de Gestión de Citas...")

def abrir_estadisticas():
    """Función para abrir el módulo de estadísticas"""
    print("Abriendo módulo de Estadísticas...")

def cerrar_sesion(ventana):
    """Cierra la sesión y regresa al login"""
    ventana.destroy()
    login.ventana_login_personalizada("Administrador", None)

def crear_encabezado_footer(ventana):
    """Crea el encabezado y pie de página"""
    
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

def mostrar_panel_admin():
    """Muestra el panel de administrador con la interfaz basada en la imagen"""
    ventana = tk.Toplevel()
    ventana.title("Panel Administrador - Fundación Corazón Down")
    ventana.geometry("960x540")
    ventana.configure(bg="white")

    crear_encabezado_footer(ventana)

    # Contenedor principal
    frame_principal = tk.Frame(ventana, bg="white")
    frame_principal.pack(expand=True, fill="both", pady=20)

    # Botón Registro de Citas
    btn_registro = Button(
        frame_principal, text="REGISTRO DE CITAS", font=("Arial", 14, "bold"),
        bg="#FF9800", fg="white", relief="flat", width=20, height=3,
        command=abrir_registro_citas
    )
    btn_registro.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Botón Gestión de Citas
    btn_gestion = Button(
        frame_principal, text="GESTIÓN DE CITAS", font=("Arial", 14, "bold"),
        bg="#3F51B5", fg="white", relief="flat", width=20, height=3,
        command=abrir_gestion_citas
    )
    btn_gestion.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # Botón Estadísticas
    btn_estadisticas = Button(
        frame_principal, text="ESTADÍSTICAS", font=("Arial", 14, "bold"),
        bg="#4CAF50", fg="white", relief="flat", width=20, height=3,
        command=abrir_estadisticas
    )
    btn_estadisticas.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    # Ajustar columnas
    frame_principal.columnconfigure(0, weight=1)
    frame_principal.columnconfigure(1, weight=1)

    # Botón de cerrar sesión
    btn_cerrar_sesion = Button(
        ventana, text="CERRAR SESIÓN", font=("Arial", 12, "bold"),
        bg="red", fg="white", relief="flat", width=20, cursor="hand2",
        command=lambda: cerrar_sesion(ventana)
    )
    btn_cerrar_sesion.pack(pady=10)

    ventana.mainloop()

# Prueba directa del panel (si se ejecuta este archivo directamente)
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal si se ejecuta directamente
    mostrar_panel_admin()
