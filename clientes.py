
import sqlite3 as sql
from colorama import Fore, init

init(autoreset=True)

def validar_edad(edad):
    """ Validar edad """
    if not edad.isdigit() or not (5 <= int(edad) <= 120):
        print(Fore.YELLOW + "Edad inválida. Debe ser un número entre 5 y 120.")
        return None
    return int(edad)


def validar_email(email):
    """ Validar email """
    if "@" not in email or "." not in email:
        print(Fore.YELLOW + "Correo electrónico inválido. Debe contener '@' y '.'")
        return None
    return email

def agregar_cliente(conexion):
    """
    Agrega un nuevo cliente a la base de datos. 
    Solicita al usuario que ingrese el nombre, apellido, edad y correo electrónico del cliente. 
    Valida que la edad esté entre 5 y 120 años y que el correo electrónico tenga un formato válido. 
    Si los datos son válidos, los inserta en la tabla clientes.
    """
    while True:
        nombre = input("Ingrese el nombre del cliente: ").strip().capitalize()
        if not nombre:
            print(Fore.YELLOW + "El nombre no puede estar vacío.")
            continue  # Si el nombre está vacío, vuelve a solicitar los datos

        apellido = input("Ingrese el apellido del cliente: ").strip().capitalize()
        if not apellido:
            print(Fore.YELLOW + "El apellido no puede estar vacío.")
            continue  # Si el apellido está vacío, vuelve a solicitar los datos

        edad = input("Ingrese la edad del cliente: ")
        edad_int = validar_edad(edad)
        if edad_int is None:
            continue  # Si la edad no es válida, vuelve a solicitar los datos


        email = input("Ingrese el correo electrónico del cliente: ").strip()
        email= validar_email(email)
        if email is None:
            continue  # Si el correo no es válido, vuelve a solicitar los datos

        try:
            cursor = conexion.cursor()
            cursor.execute('''
                INSERT INTO clientes (nombre, apellido, edad, email)
                VALUES (?, ?, ?, ?)
            ''', (nombre, apellido, edad_int, email))

            conexion.commit()
            print(Fore.GREEN + "Cliente agregado exitosamente.")
            break
            
        except sql.Error as e:
            conexion.rollback()
            print(Fore.RED + f"Error: {e}, no se pudo agregar el cliente. Intente nuevamente.")

def ver_clientes(conexion):
    """
    Muestra todos los clientes almacenados en la base de datos."""
    
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, apellido, edad, email FROM clientes ORDER BY id")
    clientes = cursor.fetchall()
    
    if not clientes:
        print(Fore.YELLOW + "\n No hay clientes cargados.")
        return

    print("\n" + "-" * 90)
    print(f"  {'ID':<5} {'NOMBRE':<20} {'APELLIDO':<20} {'EDAD':<10} {'CORREO':<30}")
    print("-" * 90)
    for id_, nombre, apellido, edad, email in clientes:
        print(f"  {id_:<5} {nombre:<20} {apellido:<20} {edad:<10} {email:<30}")
    print("-" * 90)
    print(f"  Total de clientes: {len(clientes)}")

def buscar_clientes(conexion):
    """
    Permite al usuario buscar clientes por nombre, apellido o correo electrónico.
    Solicita al usuario que ingrese un término de búsqueda y muestra los clientes que coincidan"""
    
    termino = input("Ingrese el término de búsqueda (nombre, apellido o correo electrónico): ").strip()

    if not termino:
        print(Fore.RED + " ❌ El termino de busqueda no puede estar vacio")
        return
    
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT id, nombre, apellido, edad, email FROM clientes
        WHERE nombre LIKE ? OR apellido LIKE ? OR email LIKE ?
    ''', (f'%{termino}%', f'%{termino}%', f'%{termino}%'))

    clientes = cursor.fetchall()
    if not clientes:
        print(Fore.RED + f" No se encontraron los clientes con este termino '{termino}'")
        return

    print(f"\n  Se encontraron {len(clientes)} resultado(s):")
    for id_, nombre, apellido, edad, email in clientes:
        print(f"    ID: {id_} | {nombre} | {apellido} | {edad} | {email}")

def modificar_cliente(conexion):
    """
    Permite al usuario modificar los datos de un cliente existente.
    Solicita al usuario que ingrese el ID del cliente a modificar y los nuevos datos."""
    ver_clientes(conexion)

    try:
        id_modificar = int(input("\n Ingresa el ID del cliente a modificar: ").strip())
    except ValueError:
        print(Fore.RED + " ❌ El ID debe ser un numero entero")
        return

    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, apellido, edad, email FROM clientes WHERE id = ?", (id_modificar,))
    cliente = cursor.fetchone()

    if not cliente:
        print(Fore.RED + f" ❌ No existe ningun cliente con el id {id_modificar}")
        return
    
    nombre_actual, apellido_actual, edad_actual, email_actual = cliente[1], cliente[2], cliente[3], cliente[4] 
    
    print(f"\n Cliente encontrado: {nombre_actual} {apellido_actual}, Edad: {edad_actual}, Email: {email_actual}")
    nombre_nuevo = input(f" Ingresa el nuevo nombre (dejar en blanco para mantener '{nombre_actual}'): ").strip().capitalize() or nombre_actual
    apellido_nuevo = input(f" Ingresa el nuevo apellido (dejar en blanco para mantener '{apellido_actual}'): ").strip().capitalize() or apellido_actual
    edad_nueva = input(f" Ingresa la nueva edad (dejar en blanco para mantener '{edad_actual}'): ").strip() 
    email_nuevo = input(f" Ingresa el nuevo correo electrónico (dejar en blanco para mantener '{email_actual}'): ").strip() or email_actual

    if edad_nueva == "":
        edad_nueva = int(edad_actual)
    else:
        edad_nueva = validar_edad(edad_nueva)
        if edad_nueva is None:
            return # Si la edad no es válida, vuelve a solicitar los datos
    email_nuevo = validar_email(email_nuevo)
    if email_nuevo is None:
        return  # Si el correo no es válido, vuelve a solicitar los datos

    try:
        cursor.execute('''
            UPDATE clientes
            SET nombre = ?, apellido = ?, edad = ?, email = ?
            WHERE id = ?
        ''', (nombre_nuevo, apellido_nuevo, edad_nueva, email_nuevo, id_modificar))

        conexion.commit()
        print(Fore.GREEN + f"✅ Cliente con ID {id_modificar} modificado correctamente.")
    except sql.Error as e:
        conexion.rollback()
        print(Fore.RED + f" ❌ Error al modificar el cliente: {e}")



def eliminar_cliente(conexion):
    """
    Permite al usuario eliminar un cliente de la base de datos.
    Solicita al usuario que ingrese el ID del cliente a eliminar y elimina el registro correspondiente"""
   
    ver_clientes(conexion)

    try:
        id_eliminar = int(input("\n Ingresa el ID del cliente a eliminar: ").strip()) 
    except ValueError:
        print(Fore.RED + " ❌ El ID debe ser un numero entero")
        return

    cursor = conexion.cursor()
    cursor.execute("SELECT nombre FROM clientes WHERE id = ? " , (id_eliminar,))
    fila = cursor.fetchone()

    if not fila:
        print(Fore.RED + f" ❌ No existe ningun cliente con el id {id_eliminar}")
        return

    nombre = fila[0]
    print(f"\n Cliente encontrado: {nombre}")
    respuesta = input(f" ¿ Confirmas que queres eliminar '{nombre}' (s/n): ").strip().lower()
    if respuesta != 's':
        print(Fore.YELLOW + f"Operacion cancelada.")
        return

    try:
        cursor.execute("DELETE FROM clientes WHERE id = ?",(id_eliminar,))
        conexion.commit()
        print(Fore.GREEN + f"✅ Cliente '{nombre}' eliminado correctamente.")
    except sql.Error as e:
        conexion.rollback()
        print(Fore.RED + f"\n Error al eliminar: {e}")