import re
from datetime import datetime

def confirmacion():
    """Muestra un menú para confirmar una acción.

    Returns:
        bool: True si se confirma la acción, False en caso contrario.
    """
    while True:
        try:
            match input("\n¿Está seguro? [S/N]: ").upper():
                case "S": return True
                case "N": return False
                case _: raise Exception("Opción inválida. Intente de nuevo.")
        except Exception as e: print(f"\nError: {e}")

def opcion():
    """Obtiene una opción del usuario.

    Raises:
        Exception: Opción inválida. Intente de nuevo.

    Returns:
        int: Opción del usuario.
    """
    try: return int(input("\n> "))
    except ValueError: raise Exception("Opción inválida. Intente de nuevo.")

def obtener_float(msj: str) -> float:
    """Obtiene un número flotante del usuario."""
    while True:
        try:
            raw = input(msj)
            if not raw: return 0
            return float(raw)
        except ValueError: raise Exception("\nDebe ser un número.")

def obtener_int(msj: str) -> int:
    """Obtiene un número entero del usuario."""
    while True:
        try:
            raw = input(msj)
            if not raw: return 0
            return int(raw)
        except ValueError: raise Exception("\nDebe ser un número.")

def validar_fecha(fecha: str):
    """Valida una fecha."""
    if not re.match(r"^(?!0000)\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$", fecha): raise Exception("Formato de fecha inválido. Use el formato YYYY-MM-DD.")

def cadena_a_fecha(cadena: str):
    """Convierte una cadena en formato YYYY-MM-DD a fecha."""
    return datetime.strptime(cadena, "%Y-%m-%d")