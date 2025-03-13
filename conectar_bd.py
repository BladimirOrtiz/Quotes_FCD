import mysql.connector

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Cambia esto por tu contraseña real
        database="quotes_fcd"
    )
