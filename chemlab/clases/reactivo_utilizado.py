from chemlab.utils import obtener_int

class ReactivoUtilizado:
    def __init__(self, reactivo_id, cantidad_necesaria=1, unidad_medida="mL"):
        self.reactivo_id = reactivo_id
        self.cantidad_necesaria = cantidad_necesaria
        self.unidad_medida = unidad_medida

    def __str__(self): return f"Reactivo {self.reactivo_id} - {self.cantidad_necesaria} {self.unidad_medida}"

    def editar_cantidad_necesaria(self):
        while True:
            try:
                cantidad_necesaria = obtener_int("\nCantidad necesaria: ")
                if not cantidad_necesaria: raise Exception("La cantidad necesaria no puede ser 0.")
                self.cantidad_necesaria = cantidad_necesaria
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_unidad_medida(self):
        while True:
            try:
                unidad_medida = input("\nUnidad de medida: ")
                if not unidad_medida: raise Exception("La unidad de medida no puede estar vacía.")
                self.unidad_medida = unidad_medida
                break
            except Exception as e: print(f"\nError: {e}")