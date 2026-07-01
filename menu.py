import clientes as c
import utils as u
import database as db   

def main():
    """ Función principal del programa """
    conexion = db.conectar_db()

    if conexion is None:
        print(" Error al conectar con la base de datos.")
        return

    while True:
        u.limpiar_pantalla()
        print("\n" + "=" * 50)
        print("     SISTEMA DE GESTION DE CLIENTES")
        print("=" * 50)
        print("  1. Agregar cliente")
        print("  2. Ver todos los clientes")
        print("  3. Buscar cliente")
        print("  4. Modificar cliente")
        print("  5. Eliminar cliente")
        print("  6. Salir")
        print("-" * 50)

        opcion = input("Selecciona una opcion (1-6): ").strip()

        if opcion == "1":
            c.agregar_cliente(conexion)
            u.pausar()
        elif opcion == "2":
            c.ver_clientes(conexion)
            u.pausar()
        elif opcion == "3":
            c.buscar_clientes(conexion)
            u.pausar()
        elif opcion == "4":
            c.modificar_cliente(conexion)
            u.pausar()
        elif opcion == "5":
            c.eliminar_cliente(conexion)
            u.pausar()
        elif opcion == "6":
            print("\n Hasta luego")
            break
        else:
            print(" Opcion invalida. Igresa un numero del 1 al 6")
            u.pausar()


    conexion.close()
