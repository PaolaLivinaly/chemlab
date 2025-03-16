from chemlab.utils import obtener_float

class ValorAMedir:
    def __init__(self, nombre="e", formula="e = (valor esperado - valor obtenido) / valor esperado * 100", minimo=0.98, maximo=100):
        self.nombre = nombre
        self.formula = formula
        self.minimo = minimo
        self.maximo = maximo

    def __str__(self): return f"{self.nombre} ({self.minimo} - {self.maximo}) - {self.formula}"

    def editar_nombre(self):
        while True:
            try:
                nombre = input("\nNombre: ")
                if not nombre: raise Exception("El nombre no puede estar vacío.")
                self.nombre = nombre
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_formula(self):
        while True:
            try:
                formula = input("\nFórmula: ")
                if not formula: raise Exception("La fórmula no puede estar vacía.")
                self.formula = formula
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_minimo(self):
        while True:
            try:
                minimo = obtener_float("\nMínimo: ")
                self.minimo = minimo
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_maximo(self):
        while True:
            try:
                maximo = obtener_float("\nMáximo: ")
                if not maximo: raise Exception("El máximo no puede ser 0.")
                self.maximo = maximo
                break
            except Exception as e: print(f"\nError: {e}")