from .clases import Reactivo, DB
from .utils import confirmacion, opcion, obtener_int

def obtener_siguiente_id(db: DB):
    """Obtiene el siguiente ID para un reactivo."""
    if not db.reactivos: return 1
    return max(reactivo.id for reactivo in db.reactivos) + 1

def menu(db: DB):
    """Muestra el menú de gestión de reactivos.

    Args:
        db (DB): Instancia de la base de datos.
    """
    while True:
        try:
            print("\n======== Gestión de Reactivos ========\n")
            print("1. Listar reactivos")
            print("2. Agregar reactivo")
            print("3. Modificar reactivo")
            print("4. Eliminar reactivo")
            print("5. Mostrar detalles de reactivo")
            print("6. Volver")
            match opcion():
                case 1: listar(db)
                case 2: agregar(db)
                case 3: modificar(db)
                case 4: eliminar(db)
                case 5: print(obtener_por_id(db))
                case 6: break
                case _: raise Exception("Opción inválida. Intente de nuevo.")
        except Exception as e: print(f"\nError: {e}")

def listar(db: DB):
    """Muestra reactivos."""
    if db.reactivos:
        print("\nLista de reactivos:\n")
        for reactivo in db.reactivos: print(f"{reactivo.id} - {reactivo.nombre}")
    else: print("No hay reactivos.")

def agregar(db: DB):
    """Agrega un reactivo."""
    reactivo = Reactivo(obtener_siguiente_id(db))
    reactivo.editar_nombre()
    reactivo.editar_descripcion()
    reactivo.editar_costo()
    reactivo.editar_categoria()
    reactivo.editar_unidad_medida()
    reactivo.editar_minimo_sugerido()
    reactivo.editar_inventario_disponible()
    reactivo.editar_conversiones_posibles()
    reactivo.editar_fecha_caducidad()
    db.reactivos.append(reactivo)
    print("\nReactivo agregado exitosamente.")

def modificar(db: DB):
    """Modifica un reactivo."""
    while True:
        try:
            reactivo = obtener_por_id(db) 
            if not reactivo: break 
            reactivo.editar() 
            break
        except Exception as e: print(f"\nError: {e}")

def eliminar(db: DB):
    """Elimina un reactivo."""
    while True:
        try:
            reactivo = obtener_por_id(db)
            if not reactivo or not confirmacion(): break
            db.reactivos.remove(reactivo)
            print("\nReactivo eliminado exitosamente.")
            break
        except Exception as e: print(f"\nError: {e}")

def mostrar(db: DB):
    """Muestra un reactivo."""
    while True:
        try:
            reactivo = obtener_por_id(db)
            if not reactivo: break
            print(reactivo)
            break
        except Exception as e: print(f"\nError: {e}")

def obtener_por_id(db: DB):
    """Obtiene un reactivo por ID."""
    while True:
        try:
            id_reactivo = obtener_int("\nID del reactivo (vacío para volver): ")
            if not id_reactivo: return None
            reactivo = next((reactivo for reactivo in db.reactivos if reactivo.id == id_reactivo), None)
            if not reactivo: raise Exception("Reactivo no encontrado.")
            return reactivo
        except Exception as e: print(f"\nError: {e}")