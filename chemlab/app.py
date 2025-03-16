from . import reactivos, experimentos, resultados, indicadores
from .clases import DB
from .utils import confirmacion, opcion

class App:
    def __init__(self):
        self.db = DB()

    def menu_inicial(self):
        """Muestra un menú para obtener recursos desde la API o un archivo."""
        while True:
            try:
                print("\n======== Bienvenido a ChemLab ========\n")
                print("1. Cargar recursos desde la API")
                print("2. Cargar recursos desde archivos JSON")
                print("3. Salir")
                match opcion():
                    case 1:
                        self.db.obtener_api()
                        if not self.db.reactivos: raise Exception("No se pudieron obtener los recursos.")
                        self.menu()
                    case 2:
                        self.db.obtener_archivo()
                        if not self.db.reactivos: raise Exception("No se pudieron obtener los recursos.")
                        self.menu()
                    case 3: 
                        if confirmacion(): break
                    case _: raise Exception("Opción inválida. Intente de nuevo.")
            except Exception as e: print(f"\nError: {e}")

    def menu(self):
        """Muestra el menú principal de la aplicación."""
        while True:
            try:
                print("\n======== Menú Principal ========\n")
                print("1. Gestión de reactivos")
                print("2. Gestión de experimentos")
                print("3. Gestión de resultados")
                print("4. Indicadores de gestión")
                print("5. Guardar datos")
                print("6. Salir")
                match opcion():
                    case 1: reactivos.menu(self.db)
                    case 2: experimentos.menu(self.db)
                    case 3: resultados.menu(self.db)
                    case 4: indicadores.menu(self.db)
                    case 5:
                        print("\nSe sobreescribirán los datos.")
                        if confirmacion(): self.db.guardar_datos()
                    case 6:
                        print("\nLos datos no guardados se perderán.")
                        if confirmacion(): break
                    case _: raise Exception("Opción inválida. Intente de nuevo.")
            except Exception as e: print(f"\nError: {e}")

    def iniciar(self):
        self.menu_inicial()
        print("\nGracias por usar ChemLab. ¡Hasta luego!\n")