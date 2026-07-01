import sqlite3 as sql

def conectar_db():
    """
    Conecta con la base de datos y crea la tabla clientes si no existe.
    """
    try:
        conexion = sql.connect('base_clientes.db')
        cursor = conexion.cursor()
        cursor.execute ('''
                        CREATE TABLE IF NOT EXISTS clientes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombre TEXT NOT NULL,
                            apellido TEXT NOT NULL,
                            edad INTEGER CHECK (edad >= 5 AND edad <= 120),
                            email TEXT UNIQUE CHECK (email LIKE '%@%'))
                        ''')

        conexion.commit() 
        return conexion
    
    except sql.Error as e:
        print(f"Error al conectar a la base de datos: {e}")  