import os

def limpiar_pantalla():
    """
    Limpia la pantalla de la consola."""
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    """
    Pausa la ejecución del programa hasta que el usuario presione Enter."""
    input("\n Presioná Enter para continuar...")
