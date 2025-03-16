from chemlab.utils import obtener_float

class Conversion:
    def __init__(self, unidad="L", factor=0.001):
        self.unidad = unidad
        self.factor = factor

    def editar(self):
        """Edita la conversión."""
        while True:
            try:
                self.editar_unidad()
                self.editar_factor()
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_unidad(self):
        """Edita la unidad de medida."""
        while True:
            try:
                self.unidad = input("\nUnidad de medida: ")
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_factor(self):
        """Edita el factor de conversión."""
        while True:
            try:
                self.factor = obtener_float("\nFactor de conversión: ")
                if self.factor <= 0: raise Exception("El factor de conversión debe ser mayor que 0.")
                break
            except Exception as e: print(f"\nError: {e}")
    
    def __str__(self): return f"{self.unidad} ({self.factor})"