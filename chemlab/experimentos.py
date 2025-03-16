from .clases import DB, Experimento, Receta
from .utils import confirmacion, opcion, obtener_int
import random

def menu(db: DB):
    """Muestra el menú de gestión de experimentos.

    Args:
        db (DB): Instancia de la base de datos.
    """
    while True:
        try:
            print("\n======== Gestión de Experimentos ========\n")
            print("1. Listar experimentos")
            print("2. Agregar experimento")
            print("3. Modificar experimento")
            print("4. Eliminar experimento")
            print("5. Mostrar detalles de experimento")
            print("6. Listar recetas")
            print("7. Agregar receta")
            print("8. Modificar receta")
            print("9. Eliminar receta")
            print("10. Mostrar detalles de receta")
            print("11. Volver")
            match opcion():
                case 1: listar(db)
                case 2: agregar(db)
                case 3: modificar(db)
                case 4: eliminar(db)
                case 5: print(obtener_por_id(db))
                case 6: listar_recetas(db)
                case 7: agregar_receta(db)
                case 8: modificar_receta(db)
                case 9: eliminar_receta(db)
                case 10: print(obtener_receta_por_id(db))
                case 11: break
                case _: raise Exception("Opción inválida. Intente de nuevo.")
        except Exception as e: print(f"\nError: {e}")

def listar(db: DB):
    """Muestra experimentos."""
    if db.experimentos:
        print("\nLista de experimentos:\n")
        for experimento in db.experimentos: print(f'{experimento.id} - {next((receta.nombre for receta in db.recetas if receta.id == experimento.receta_id), "Receta no encontrada")} - {", ".join(experimento.personas_responsables)}')
    else: print("No hay experimentos.")

def agregar(db: DB):
    """Agrega un experimento."""
    experimento = Experimento(obtener_siguiente_id(db))
    receta: Receta  = experimento.editar_receta_id(db)
    if not receta: return
    for reactivo_utilizado in receta.reactivos_utilizados:
        reactivo = next((reactivo for reactivo in db.reactivos if reactivo.id == reactivo_utilizado.reactivo_id), None)
        if reactivo:
            if reactivo_utilizado.cantidad_necesaria > reactivo.inventario_disponible:
                print(f"\nNo hay suficiente {reactivo.nombre} en inventario. Se cancelará el experimento.")
                return
            rand = random.uniform(0.001, 0.225)
            descuento = reactivo_utilizado.cantidad_necesaria * (1 + rand)
            if reactivo.inventario_disponible < descuento: descuento = reactivo.inventario_disponible
            reactivo.inventario_disponible -= descuento
            print(f"\nSe han utilizado {descuento} {reactivo.unidad_medida} de {reactivo.nombre}.")
            reactivo.comprobar_inventario()
    experimento.editar_personas_responsables()
    experimento.editar_fecha()
    experimento.editar_costo_asociado()
    experimento.editar_resultado()
    db.experimentos.append(experimento)
    print("\nExperimento agregado exitosamente.")

def modificar(db: DB):
    """Modifica un experimento."""
    while True:
        try:
            experimento = obtener_por_id(db)
            if not experimento: break
            experimento.editar(db)
            break
        except Exception as e: print(f"\nError: {e}")

def eliminar(db: DB):
    """Elimina un experimento."""
    while True:
        try:
            experimento = obtener_por_id(db)
            if not experimento: break
            if confirmacion():
                db.experimentos.remove(experimento)
                print("\nExperimento eliminado exitosamente.")
            break
        except Exception as e: print(f"\nError: {e}")

def obtener_por_id(db: DB):
    """Obtiene un experimento por su ID.

    Args:
        db (DB): Instancia de la base de datos.

    Returns:
        Experimento: Instancia del experimento.
    """
    while True:
        try:
            experimento_id = obtener_int("\nID experimento (vacío para volver): ")
            if not experimento_id: return None
            experimento = next((experimento for experimento in db.experimentos if experimento.id == experimento_id), None)
            if not experimento: raise Exception("El experimento no existe.")
            return experimento
        except Exception as e: print(f"\nError: {e}")

def obtener_siguiente_id(db: DB):
    """Obtiene el siguiente ID de experimento.

    Args:
        db (DB): Instancia de la base de datos.

    Returns:
        int: ID del experimento.
    """
    return max((experimento.id for experimento in db.experimentos), default=0) + 1

def listar_recetas(db: DB):
    """Muestra recetas."""
    if db.recetas:
        print("\nLista de recetas:\n")
        for receta in db.recetas: print(f"{receta.id} - {receta.nombre}")
    else: print("No hay recetas.")

def agregar_receta(db: DB):
    """Agrega una receta."""
    receta = Receta(obtener_siguiente_id_receta(db))
    receta.editar_nombre()
    receta.editar_objetivo()
    receta.editar_reactivos_utilizados(db)
    receta.editar_procedimiento()
    receta.editar_valores_a_medir()
    db.recetas.append(receta)
    print("\nReceta agregada exitosamente.")

def modificar_receta(db: DB):
    """Modifica una receta."""
    while True:
        try:
            receta = obtener_receta_por_id(db)
            if not receta: break
            receta.editar(db)
            break
        except Exception as e: print(f"\nError: {e}")

def eliminar_receta(db: DB):
    """Elimina una receta."""
    while True:
        try:
            receta = obtener_receta_por_id(db)
            if not receta: break
            print("\nSe eliminará la receta y todos los experimentos asociados.")
            if confirmacion():
                db.recetas.remove(receta)
                db.experimentos = [experimento for experimento in db.experimentos if experimento.receta_id != receta.id]
                print("\nReceta y experimentos asociados eliminados exitosamente.")
            break
        except Exception as e: print(f"\nError: {e}")

def obtener_receta_por_id(db: DB):
    """Obtiene una receta por su ID.

    Args:
        db (DB): Instancia de la base de datos.

    Returns:
        Receta: Instancia de la receta.
    """
    while True:
        try:
            receta_id = obtener_int("\nID receta (vacío para volver): ")
            if not receta_id: return None
            receta = next((receta for receta in db.recetas if receta.id == receta_id), None)
            if not receta: raise Exception("La receta no existe.")
            return receta
        except Exception as e: print(f"\nError: {e}")

def obtener_siguiente_id_receta(db: DB):
    """Obtiene el siguiente ID de receta.

    Args:
        db (DB): Instancia de la base de datos.

    Returns:
        int: ID de la receta.
    """
    return max((receta.id for receta in db.recetas), default=0) + 1
