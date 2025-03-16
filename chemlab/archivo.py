import json
from .clases import Reactivo, Experimento, Receta, Conversion, ValorAMedir, ReactivoUtilizado

RUTA_REACTIVOS = "chemlab/json/reactivos.json"
RUTA_EXPERIMENTOS = "chemlab/json/experimentos.json"
RUTA_RECETAS = "chemlab/json/recetas.json"

def obtener_reactivos():
    """Obtiene reactivos desde un archivo JSON

    Returns:
        list: Lista de reactivos.
    """
    try:
        reactivos = [Reactivo(**reactivo) for reactivo in json.load(open(RUTA_REACTIVOS, 'r', encoding="utf-8"))]
        for reactivo in reactivos: reactivo.conversiones_posibles = [Conversion(**conversion) for conversion in reactivo.conversiones_posibles]
        print("\nReactivos obtenidos exitosamente.")
        return reactivos
    except Exception as e:
        print(f"\nError al cargar reactivos: {e}")
        return []

def obtener_experimentos():
    """Obtiene experimentos desde un archivo JSON

    Returns:
        list: Lista de experimentos.
    """
    try:
        experimentos = [Experimento(**experimento) for experimento in json.load(open(RUTA_EXPERIMENTOS, 'r', encoding="utf-8"))]
        print("\nExperimentos obtenidos exitosamente.")
        return experimentos
    except Exception as e:
        print(f"\nError al cargar experimentos: {e}")
        return []

def obtener_recetas():
    """Obtiene recetas desde un archivo JSON

    Returns:
        list: Lista de recetas.
    """
    try:
        recetas =  [Receta(**receta) for receta in json.load(open(RUTA_RECETAS, 'r', encoding="utf-8"))]
        for receta in recetas: receta.reactivos_utilizados = [ReactivoUtilizado(**reactivo) for reactivo in receta.reactivos_utilizados]
        for receta in recetas: receta.valores_a_medir = [ValorAMedir(**valor) for valor in receta.valores_a_medir]
        print("\nRecetas obtenidas exitosamente.")
        return recetas
    except Exception as e:
        print(f"\nError al cargar recetas: {e}")
        return []

def guardar_reactivos(reactivos):
    """Guarda reactivos en un archivo JSON.

    Args:
        reactivos (list): Lista de reactivos.
    """
    try:
        datos = []
        for reactivo in reactivos:
            # Create a dictionary copy of reactivo
            reactivo_dict = reactivo.__dict__.copy()
            reactivo_dict["conversiones_posibles"] = [conversion.__dict__ for conversion in reactivo.conversiones_posibles]
            datos.append(reactivo_dict)
        json.dump(datos, open(RUTA_REACTIVOS, 'w', encoding="utf-8"), indent=4)
        print("\nReactivos guardados exitosamente.")
    except Exception as e:
        print(f"\nError al guardar reactivos: {e}")

def guardar_experimentos(experimentos):
    """Guarda experimentos en un archivo JSON.

    Args:
        experimentos (list): Lista de experimentos.
    """
    try:
        json.dump([experimento.__dict__ for experimento in experimentos], open(RUTA_EXPERIMENTOS, 'w', encoding="utf-8"), indent=4)
        print("\nExperimentos guardados exitosamente.")
    except Exception as e:
        print(f"\nError al guardar experimentos: {e}")

def guardar_recetas(recetas):
    """Guarda recetas en un archivo JSON.

    Args:
        recetas (list): Lista de recetas.
    """
    try:
        datos = []
        for receta in recetas:
            receta_dict = receta.__dict__.copy()
            receta_dict["reactivos_utilizados"] = [reactivo.__dict__ for reactivo in receta.reactivos_utilizados]
            receta_dict["valores_a_medir"] = [valor.__dict__ for valor in receta.valores_a_medir]
            datos.append(receta_dict)
        print("\nRecetas guardadas exitosamente.")
    except Exception as e:
        print(f"\nError al guardar recetas: {e}")