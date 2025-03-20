import tkinter as tk
from tkinter import Button, Label
import login  # Para cerrar sesión y volver al login

def cerrar_sesion(ventana, root):
    """Cierra la sesión y regresa al login"""
    ventana.destroy()
    root.deiconify()  # ✅ Muestra la ventana principal de nuevo
    login.ventana_login_personalizada("Administrador", root)

def mostrar_panel_admin(ventana, root):
    """Muestra el panel de administrador"""
    ventana.title("Panel Administrador - Fundación Corazón Down")
    ventana.geometry("960x540")
    ventana.configure(bg="white")

    Label(ventana, text="Bienvenido al Panel Administrador", font=("Arial", 16, "bold"), bg="white").pack(pady=20)

    btn_cerrar_sesion = Button(
        ventana, text="CERRAR SESIÓN", font=("Arial", 12, "bold"),
        bg="red", fg="white", relief="flat", width=20, cursor="hand2",
        command=lambda: cerrar_sesion(ventana, root)  # ✅ Pasamos `root`
    )
    btn_cerrar_sesion.pack(pady=10)

    ventana.mainloop()  # ✅ Mantiene la ventana abierta
