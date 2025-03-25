import tkinter as tk
from tkinter import Frame, Label, Button, PhotoImage
from tkinter import ttk, messagebox
import webbrowser
from tkcalendar import DateEntry
import os
import locale

locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

# ─── Simulación de datos ───
pacientes = {"Juan Pérez": 8, "Ana Torres": 10, "Luis Gómez": 6}
terapeutas = ["Lic. Miriam", "Lic. Antonio", "Lic. Sofía"]
areas = ["Psicología", "Ocupacional", "Física", "Lenguaje", "Lectoescritura"]
pagos_a = ["Caja A", "Caja B", "Caja C"]

def abrir_url(url):
    webbrowser.open(url)

def registrar_cita():
    messagebox.showinfo("Registro", "Cita registrada exitosamente.")

def agregar_paciente():
    messagebox.showinfo("Agregar", "Paciente añadido exitosamente.")

def ventana_registro_cita():
    ventana = tk.Toplevel()
    ventana.title("Registro de Cita - Fundación Corazón Down")
    ventana.geometry("1000x650")
    ventana.configure(bg="white")

    # ───── ENCABEZADO ─────
    encabezado = Frame(ventana, bg="#2E3B55", height=80)
    encabezado.pack(fill="x")

    try:
        ventana.logo_izq = PhotoImage(file="icono/logofcd.png").subsample(5, 5)
        ventana.logo_der = PhotoImage(file="icono/logo.png").subsample(5, 5)
    except Exception as e:
        print("Error cargando logos:", e)
        ventana.logo_izq = ventana.logo_der = None

    if ventana.logo_izq:
        Label(encabezado, image=ventana.logo_izq, bg="#2E3B55").pack(side="left", padx=10)

    Label(encabezado, text="SISTEMA DE REGISTRO DE CITAS\n(FUNDACIÓN CORAZÓN DOWN)",
          font=("Arial", 14, "bold"), bg="#2E3B55", fg="white", justify="center").pack(side="left", expand=True)

    if ventana.logo_der:
        Label(encabezado, image=ventana.logo_der, bg="#2E3B55").pack(side="right", padx=10)

    # ───── TÍTULO ─────
    Label(ventana, text="REGISTRO DE CITA", font=("Arial", 18, "bold"), bg="white", pady=10).pack()

    # ───── FORMULARIO ─────
    form_frame = Frame(ventana, bg="white")
    form_frame.pack(pady=10)

    def actualizar_edad(event):
        nombre = combo_paciente.get()
        edad = pacientes.get(nombre, "")
        entry_edad.config(state="normal")
        entry_edad.delete(0, tk.END)
        entry_edad.insert(0, str(edad))
        entry_edad.config(state="readonly")

    # ───── Fila 1 ─────
    ttk.Label(form_frame, text="Nombre del Paciente").grid(row=0, column=0, sticky="w", padx=10)
    combo_paciente = ttk.Combobox(form_frame, values=list(pacientes.keys()), width=30, state="readonly")
    combo_paciente.grid(row=1, column=0, padx=10, pady=5)
    combo_paciente.bind("<<ComboboxSelected>>", actualizar_edad)

    ttk.Label(form_frame, text="Edad").grid(row=0, column=1, sticky="w")
    entry_edad = ttk.Entry(form_frame, width=30, state="readonly")
    entry_edad.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(form_frame, text="Área Terapéutica").grid(row=0, column=2, sticky="w")
    combo_area = ttk.Combobox(form_frame, values=areas, width=30, state="readonly")
    combo_area.grid(row=1, column=2, padx=10, pady=5)

    # ───── Fila 2 ─────
    ttk.Label(form_frame, text="Terapeuta titular").grid(row=2, column=0, sticky="w", padx=10)
    combo_terapeuta = ttk.Combobox(form_frame, values=terapeutas, width=30, state="readonly")
    combo_terapeuta.grid(row=3, column=0, padx=10, pady=5)

    ttk.Label(form_frame, text="Fecha").grid(row=2, column=1, sticky="w")
    entry_fecha = DateEntry(form_frame, width=27, background='darkblue', foreground='white',
                            borderwidth=2, date_pattern='dd/mm/yyyy', locale='es')
    entry_fecha.grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(form_frame, text="Hora").grid(row=2, column=2, sticky="w")
    hora_frame = Frame(form_frame, bg="white")
    hora_frame.grid(row=3, column=2, padx=10, pady=5, sticky="w")

    spin_hora = ttk.Spinbox(hora_frame, from_=1, to=12, width=5, format="%02.0f")
    spin_hora.grid(row=0, column=0)
    Label(hora_frame, text=":", bg="white").grid(row=0, column=1)
    spin_min = ttk.Spinbox(hora_frame, from_=0, to=59, width=5, format="%02.0f")
    spin_min.grid(row=0, column=2, padx=(5, 0))
    combo_am_pm = ttk.Combobox(hora_frame, values=["AM", "PM"], width=5, state="readonly")
    combo_am_pm.grid(row=0, column=3, padx=(5, 0))

    # ───── Fila 3 ─────
    ttk.Label(form_frame, text="Tutor del Paciente").grid(row=4, column=0, sticky="w", padx=10)
    entry_tutor = ttk.Entry(form_frame, width=30)
    entry_tutor.grid(row=5, column=0, padx=10, pady=5)

    ttk.Label(form_frame, text="Tel. del Tutor").grid(row=4, column=1, sticky="w")
    entry_tel = ttk.Entry(form_frame, width=30)
    entry_tel.grid(row=5, column=1, padx=10, pady=5)

    ttk.Label(form_frame, text="Pago a").grid(row=4, column=2, sticky="w")
    combo_pago = ttk.Combobox(form_frame, values=pagos_a, width=30, state="readonly")
    combo_pago.grid(row=5, column=2, padx=10, pady=5)

    # ───── Fila 4 ─────
    ttk.Label(form_frame, text="Importe").grid(row=6, column=0, sticky="w", padx=10)
    entry_importe = ttk.Entry(form_frame, width=30)
    entry_importe.grid(row=7, column=0, padx=10, pady=5)

    ttk.Label(form_frame, text="Observaciones").grid(row=6, column=1, sticky="w")
    entry_obs = ttk.Entry(form_frame, width=65)
    entry_obs.grid(row=7, column=1, columnspan=2, padx=10, pady=5)

    # ───── BOTONES ─────
    boton_frame = Frame(ventana, bg="white")
    boton_frame.pack(pady=10)
    ttk.Button(boton_frame, text="AGREGAR PACIENTE", command=agregar_paciente).grid(row=0, column=0, padx=20)
    ttk.Button(boton_frame, text="REGISTRAR CITA", command=registrar_cita).grid(row=0, column=1, padx=20)

    # ───── FOOTER COMPLETO ─────
    footer = tk.Frame(ventana, bg="#D50000", height=120)
    footer.pack(side="bottom", fill="x")

    footer_content = tk.Frame(footer, bg="#D50000")
    footer_content.pack(fill="x")

    ruta_logo_footer = os.path.join("icono", "logofcd.png")
    try:
        logo_footer = tk.PhotoImage(file=ruta_logo_footer).subsample(5, 5)
    except:
        logo_footer = None

    if logo_footer:
        lbl_logo_footer = tk.Label(footer_content, image=logo_footer, bg="#D50000")
        lbl_logo_footer.image = logo_footer
        lbl_logo_footer.pack(side="left", padx=20, pady=5)

    info_frame = tk.Frame(footer_content, bg="#D50000")
    info_frame.pack(side="left", expand=True)

    tk.Label(info_frame, text="XICOTÉNCATL 1017, BARRIO DE LA NORIA, OAXACA",
             font=("Arial", 9, "bold"), bg="#D50000", fg="white").pack(pady=(10, 5))

    redes = {
        "Facebook": ("icono/ficon.png", "https://www.facebook.com/FundacionCorazonDown"),
        "Instagram": ("icono/insicon.png", "https://www.instagram.com/fundacioncorazondown"),
        "TikTok": ("icono/ticon.png", "https://www.tiktok.com/@corazndown")
    }

    redes_frame = tk.Frame(info_frame, bg="#D50000")
    redes_frame.pack()

    for red, (img_path, url) in redes.items():
        try:
            icono = tk.PhotoImage(file=img_path).subsample(2, 2)
            btn = tk.Button(redes_frame, image=icono, bg="#D50000", relief="flat", command=lambda u=url: abrir_url(u))
            btn.image = icono
            btn.pack(side="left", padx=5)
        except:
            pass

# ───── MAIN ─────
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    ventana_registro_cita()
    root.mainloop()
