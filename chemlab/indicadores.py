from .utils import opcion, cadena_a_fecha
from .clases import DB

"""
Genera estadísticas y/o gráficos sobre la actividad del laboratorio: uso de
reactivos, número de experimentos realizados, nivel de cumplimiento en medidas de
seguridad, etc.
1. Determinar los investigadores que más utilizan el laboratorio
2. Determinar el experimentos más hecho y el menos hecho
3. Determinar los 5 reactivos con más alta rotación
4. Determinar los 3 reactivos con mayor desperdicio
5. Determinar los reactivos que más se vencen
6. Determinar cuántas veces no se logró hacer un experimento por falta de
reactivos
7. Realizar gráficos con dichas estadísticas con las librerías de matplotlib o
Bokeh (Bono).
"""

def menu(db: DB):
    """Muestra el menú de gestión de indicadores.

    Args:
        db (DB): Instancia de la base de datos.
    """
    while True:
        try:
            print("\n======== Indicadores de Gestión ========\n")
            print("1. Investigadores que más utilizan el laboratorio")
            print("2. Experimentos más y menos realizado")
            print("3. Reactivos con más alta rotación")
            print("4. Reactivos con mayor desperdicio")
            print("5. Reactivos que más se vencen")
            print("6. Experimentos no realizados por falta de reactivos")
            print("7. Volver")
            match opcion():
                case 1: investigadores_mas_utilizan(db)
                case 2: experimentos_mas_menos(db)
                case 3: reactivos_alta_rotacion(db)
                case 4: reactivos_mayor_desperdicio(db)
                case 5: reactivos_mas_vencen(db)
                case 6: experimentos_no_realizados(db)
                case 7: break
                case _: raise Exception("Opción inválida. Intente de nuevo.")
        except Exception as e: print(f"\nError: {e}")

def investigadores_mas_utilizan(db: DB):
    """Determina los investigadores que más utilizan el laboratorio."""
    if db.experimentos:
        investigadores = {}
        for experimento in db.experimentos:
            for investigador in experimento.personas_responsables:
                if investigador in investigadores: investigadores[investigador] += 1
                else: investigadores[investigador] = 1
        if investigadores:
            print("\nInvestigadores que más utilizan el laboratorio:\n")
            for investigador, cantidad in sorted(investigadores.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"{investigador} - {cantidad} experimentos")
        else: print("No hay investigadores.")
    else: print("No hay experimentos.")

def experimentos_mas_menos(db: DB):
    """Determina los experimentos más y menos realizados."""
    if db.experimentos:
        experimentos = {}
        for experimento in db.experimentos:
            if experimento.receta_id in experimentos: experimentos[experimento.receta_id] += 1
            else: experimentos[experimento.receta_id] = 1
        if experimentos:
            print("\nExperimento más realizado:")
            receta_mas = next(receta for receta in db.recetas if receta.id == max(experimentos, key=experimentos.get))
            print(f"{receta_mas.nombre} - {experimentos[receta_mas.id]} veces")
            print("\nExperimento menos realizado:")
            receta_menos = next(receta for receta in db.recetas if receta.id == min(experimentos, key=experimentos.get))
            print(f"{receta_menos.nombre} - {experimentos[receta_menos.id]} veces")
        else: print("No hay experimentos.")
    else: print("No hay experimentos.")

def reactivos_alta_rotacion(db: DB):
    """Determina los reactivos con más alta rotación."""
    if db.experimentos:
        reactivos = {}
        for experimento in db.experimentos:
            for reactivo in obtener_reactivos_de_experimento(db, experimento):
                if reactivo.nombre in reactivos: reactivos[reactivo.nombre] += 1
                else: reactivos[reactivo.nombre] = 1
        if reactivos:
            print("\nReactivos con más alta rotación:\n")
            for reactivo, cantidad in sorted(reactivos.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"{reactivo} - {cantidad} veces")
        else: print("No hay reactivos.")
    else: print("No hay experimentos.")

def obtener_reactivos_de_receta(db: DB, receta):
    """Obtiene los reactivos utilizados en una receta.

    Args:
        db (DB): Instancia de la base de datos.
        receta (Receta): Instancia de una receta.

    Returns:
        list: Lista de reactivos.
    """
    ids = [reactivo.reactivo_id for reactivo in receta.reactivos_utilizados]
    return [reactivo for reactivo in db.reactivos if reactivo.id in ids]

def obtener_reactivos_de_experimento(db: DB, experimento):
    """Obtiene los reactivos utilizados en un experimento.

    Args:
        db (DB): Instancia de la base de datos.
        experimento (Experimento): Instancia de un experimento.

    Returns:
        list: Lista de reactivos.
    """
    receta = next((receta for receta in db.recetas if receta.id == experimento.receta_id), None)
    return obtener_reactivos_de_receta(db, receta)

def reactivos_mayor_desperdicio(db: DB):
    """Determina los reactivos con mayor desperdicio."""
    if db.experimentos:
        reactivos = {}
        for experimento in db.recetas:
            for reactivo in obtener_reactivos_de_receta(db, experimento):
                if reactivo.nombre in reactivos: reactivos[reactivo.nombre] += 1
                else: reactivos[reactivo.nombre] = 1
        if reactivos:
            print("\nReactivos con mayor desperdicio:\n")
            sort = sorted(reactivos.items(), key=lambda x: x[1], reverse=True)
            for reactivo, cantidad in sort[:3]:
                print(f"{reactivo} - {cantidad} veces")
        else: print("No hay reactivos.")
    else: print("No hay experimentos.")

def reactivos_mas_vencen(db: DB):
    """Determina los reactivos que más se vencen."""
    if db.reactivos:
        print("\nReactivos que más se vencen:\n")
        for reactivo in sorted(db.reactivos, key=lambda x: cadena_a_fecha(x.fecha_caducidad))[:5]:
            print(f"{reactivo.nombre} - {reactivo.fecha_caducidad}")
    else: print("No hay reactivos.")

def experimentos_no_realizados(db: DB):
    """Determina los experimentos que no pueden realizarse por falta de reactivos."""
    if db.recetas:
        recetas = []
        for receta in db.recetas:
            for reactivo_receta in receta.reactivos_utilizados:
                if reactivo_receta.cantidad_necesaria > obtener_reactivo_por_id(db, reactivo_receta.reactivo_id).inventario_disponible:
                    recetas.append(receta)
                    break
        if recetas:
            print("\nExperimentos que no pueden realizarse por falta de reactivos:\n")
            for receta in recetas: print(f"{receta.nombre}")
        else: print("\nNo hay experimentos que no pueden realizarse.")
    else: print("\nNo hay experimentos.")

def obtener_reactivo_por_id(db, id):
    """Obtiene un reactivo por ID.

    Returns:
        Reactivo: Instancia de un reactivo.
    """
    return next(reactivo for reactivo in db.reactivos if reactivo.id == id)