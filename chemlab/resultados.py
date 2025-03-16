from .utils import opcion, obtener_float
from .clases import DB
from . import experimentos
import matplotlib.pyplot as plt

def menu(db: DB):
    """Muestra el menú de gestión de resultados.

    Args:
        db (DB): Instancia de la base de datos.
    """
    while True:
        try:
            print("\n======== Gestión de Resultados ========\n")
            print("1. Evaluar resultado")
            print("2. Volver")
            match opcion():
                case 1: evaluar(db)
                case 2: break
                case _: raise Exception("Opción inválida. Intente de nuevo.")
        except Exception as e: print(f"\nError: {e}")

def evaluar(db: DB):
    """Evalúa un resultado."""
    experimento = experimentos.obtener_por_id(db)
    if not experimento: return
    receta = next((receta for receta in db.recetas if receta.id == experimento.receta_id), None)
    if not receta:
        print("\nNo se encontró la receta de este experimento.")
        return
    if not receta.valores_a_medir:
        print("\nLa receta no tiene valores a medir.")
        return
    print("\nSe evaluará el siguiente experimento:")
    print(experimento)
    invalido = False

    _, ax = plt.subplots(figsize=(10, 5))
    y_positions = range(len(receta.valores_a_medir))

    for i, valor_a_medir in enumerate(receta.valores_a_medir):
        valor = obtener_float(f"\n¿Cuál fue el resultado de {valor_a_medir.nombre}?: ")
        if valor < valor_a_medir.minimo or valor > valor_a_medir.maximo:
            print(f"\nEl resultado de {valor_a_medir.nombre} está fuera de los parámetros aceptables ({valor_a_medir.minimo} - {valor_a_medir.maximo}).")
            invalido = True
        else: print(f"\nEl resultado de {valor_a_medir.nombre} está dentro de los parámetros aceptables ({valor_a_medir.minimo} - {valor_a_medir.maximo}).")
        
        ax.hlines(y=i, xmin=valor_a_medir.minimo, xmax=valor_a_medir.maximo, color='lightgreen', lw=10, label='Intervalo Aceptado' if i == 0 else "")
        ax.plot(valor, i, 'ro', markersize=2, label='Valor Calculado' if i == 0 else "")

    if invalido: print("\nEl experimento no estuvo dentro de los parámetros aceptables.")
    else: print("\nEl experimento estuvo dentro de los parámetros aceptables.")

    ax.set_yticks(list(y_positions))
    ax.set_yticklabels([valor.nombre for valor in receta.valores_a_medir])
    ax.set_title("Resultados del experimento")
    ax.legend()
    plt.show()