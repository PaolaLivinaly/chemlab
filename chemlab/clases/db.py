class DB:
    def __init__(self):
        self.reactivos = []
        self.experimentos = []
        self.recetas = []

    def obtener_api(self):
        """Obtiene reactivos, experimentos y recetas desde la API."""
        from chemlab import api
        self.reactivos = api.obtener_reactivos()
        self.experimentos = api.obtener_experimentos()
        self.recetas = api.obtener_recetas()

    def obtener_archivo(self):
        """Obtiene reactivos, experimentos y recetas desde un archivo JSON."""
        from chemlab import archivo
        self.reactivos = archivo.obtener_reactivos()
        self.experimentos = archivo.obtener_experimentos()
        self.recetas = archivo.obtener_recetas()

    def guardar_datos(self):
        """Guarda reactivos, experimentos y recetas en archivos JSON."""
        from chemlab import archivo
        archivo.guardar_reactivos(self.reactivos)
        archivo.guardar_experimentos(self.experimentos)
        archivo.guardar_recetas(self.recetas)