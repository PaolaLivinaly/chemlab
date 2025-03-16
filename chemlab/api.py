import requests
from .clases import Reactivo, Experimento, Receta, Conversion, ValorAMedir, ReactivoUtilizado

def url(recurso):
    """Obtiene la URL de un recurso de la API.

    Args:
        recurso (str): Nombre del recurso.

    Returns:
        str: URL del recurso.
    """
    return f"https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/refs/heads/main/{recurso}.json"

def obtener_reactivos():
    """Obtiene reactivos desde la API.

    Returns:
        list: Lista de reactivos.
    """
    try:
        reactivos = [Reactivo(**reactivo) for reactivo in requests.get(url("reactivos")).json()]
        for reactivo in reactivos: reactivo.conversiones_posibles = [Conversion(**conversion) for conversion in reactivo.conversiones_posibles]
        print("\nReactivos obtenidos exitosamente desde la API.")
        return reactivos
    except Exception as e:
        print(f"\nError al obtener reactivos desde la API: {e}")
        return []

def obtener_experimentos():
    """Obtiene experimentos desde la API.

    Returns:
        list: Lista de experimentos.
    """
    try:
        experimentos = [Experimento(**experimento) for experimento in requests.get(url("experimentos")).json()]
        print("\nExperimentos obtenidos exitosamente desde la API.")
        return experimentos
    except Exception as e:
        print(f"\nError al obtener experimentos desde la API: {e}")
        return []

def obtener_recetas():
    """Obtiene recetas desde la API.

    Returns:
        list: Lista de recetas.
    """
    try:
        recetas = [Receta(**receta) for receta in requests.get(url("recetas")).json()]
        for receta in recetas: receta.reactivos_utilizados = [ReactivoUtilizado(**reactivo) for reactivo in receta.reactivos_utilizados]
        for receta in recetas: receta.valores_a_medir = [ValorAMedir(**valor) for valor in receta.valores_a_medir]
        print("\nRecetas obtenidas exitosamente desde la API.")
        return recetas
    except Exception as e:
        print(f"\nError al obtener recetas desde la API: {e}")
        return []
