from chemlab.utils import opcion, obtener_float, validar_fecha
from chemlab.clases.conversion import Conversion

class Reactivo:
    """Representa un reactivo."""
    def __init__(self, id, nombre="Reactivo Genérico", descripcion="", costo=1, categoria="", inventario_disponible=1, unidad_medida="g", fecha_caducidad="", minimo_sugerido=0, conversiones_posibles: list[Conversion]=[]):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.costo = costo
        self.categoria = categoria
        self.inventario_disponible = inventario_disponible
        self.unidad_medida = unidad_medida
        self.fecha_caducidad = fecha_caducidad
        self.minimo_sugerido = minimo_sugerido
        self.conversiones_posibles = conversiones_posibles

    def __str__(self):
        conversiones_posibles = ''
        if self.conversiones_posibles:
            for conversion in self.conversiones_posibles: conversiones_posibles += "\n- " + conversion.__str__()
        return (f"\n--- Reactivo {self.id} ---\n"
                f"Nombre: {self.nombre}\n"
                f"Descripción: {self.descripcion}\n"
                f"Costo: {self.costo}\n"
                f"Categoría: {self.categoria}\n"
                f"Inventario: {self.inventario_disponible} {self.unidad_medida}\n"
                f"Fecha de caducidad: {self.fecha_caducidad if self.fecha_caducidad else 'No aplica'}\n"
                f"Mínimo sugerido: {self.minimo_sugerido} {self.unidad_medida}\n"
                f"Conversiones posibles: {conversiones_posibles}")

    def comprobar_inventario(self):
        """Determina si el reactivo necesita reposición."""
        if self.inventario_disponible <= self.minimo_sugerido: print(f"\nEl reactivo {self.nombre} [{self.id}] necesita reposición.")

    def editar(self):
        while True:
            try:
                print(self)
                print("\n¿Qué desea editar?\n")
                print("1. Nombre")
                print("2. Descripción")
                print("3. Costo")
                print("4. Categoría")
                print("5. Inventario disponible")
                print("6. Unidad de medida")
                print("7. Fecha de caducidad")
                print("8. Mínimo sugerido")
                print("9. Conversiones posibles")
                print("10. Volver")
                match opcion():
                    case 1: self.editar_nombre()
                    case 2: self.editar_descripcion()
                    case 3: self.editar_costo()
                    case 4: self.editar_categoria()
                    case 5: self.editar_inventario_disponible()
                    case 6: self.cambiar_unidad_medida()
                    case 7: self.editar_fecha_caducidad()
                    case 8: self.editar_minimo_sugerido()
                    case 9: 
                        self.mostrar_conversiones()
                        self.editar_conversiones_posibles()
                    case 10: break
                    case _: raise Exception("Opción inválida. Intente de nuevo.")
                print("\nEdición exitosa.")
                self.comprobar_inventario()
            except Exception as e: print(f"\nError: {e}")

    def editar_nombre(self):
        """Edita el nombre del reactivo."""
        while True:
            try:
                nombre = input("\nNombre: ")
                if not nombre: raise Exception("El nombre no puede estar vacío.")
                self.nombre = nombre
                break
            except Exception as e: print(f"\nError: {e}")
    
    def editar_descripcion(self):
        """Edita la descripción del reactivo."""
        while True:
            try:
                self.descripcion = input("\nDescripción: ")
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_costo(self):
        """Edita el costo del reactivo."""
        while True:
            try:
                costo = obtener_float("\nCosto: ")
                if costo <= 0: raise Exception("El costo debe ser mayor que 0.")
                self.costo = costo
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_categoria(self):
        """Edita la categoría del reactivo."""
        while True:
            try:
                self.categoria = input("\nCategoría: ")
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_inventario_disponible(self):
        """Edita el inventario disponible del reactivo."""
        while True:
            try:
                inventario_disponible = obtener_float("\nInventario disponible: ")
                if inventario_disponible < 0: raise Exception("El inventario disponible no puede ser negativo.")
                self.inventario_disponible = inventario_disponible
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_unidad_medida(self):
        """Edita la unidad de medida del reactivo."""
        while True:
            try:
                self.unidad_medida = input("\nUnidad de medida: ")
                break
            except Exception as e: print(f"\nError: {e}")

    def cambiar_unidad_medida(self):
        """Cambia la unidad de medida del reactivo."""
        while True:
            try:
                # Si no hay conversiones posibles, no se puede cambiar la unidad de medida
                if not self.conversiones_posibles:
                    print("\nNo hay conversiones disponibles.")
                    break
                
                # Mostrar conversiones posibles
                print(f"\nUnidad actual: {self.unidad_medida}")
                self.mostrar_conversiones()

                # Obtener unidad de conversión
                unidad = input("\nUnidad de conversión (vacío para volver): ")

                # Si la unidad es vacía, salir
                if not unidad: break

                # Obtener conversión
                conversion = self.obtener_conversion(unidad)

                # Si la conversión no existe, mostrar error
                if not conversion: raise Exception("La conversión no existe.")
                
                # Convertir las demás conversiones correspondientemente
                self.conversiones_posibles.remove(conversion)
                nueva_conversion = Conversion(self.unidad_medida, 1 / conversion.factor)
                for c in self.conversiones_posibles: c.factor *= nueva_conversion.factor
                self.conversiones_posibles.append(nueva_conversion)

                # Convertir el inventario disponible y el mínimo sugerido
                self.inventario_disponible *= conversion.factor
                self.minimo_sugerido *= conversion.factor
                self.unidad_medida = conversion.unidad

                print("\nUnidad de medida cambiada exitosamente.")
                break
            except Exception as e: print(f"\nError: {e}")
    
    def editar_fecha_caducidad(self):
        """Edita la fecha de caducidad del reactivo."""
        while True:
            try:
                fecha = input("\nFecha de caducidad (YYYY-MM-DD): ")
                if not fecha:
                    self.fecha_caducidad = ""
                    break
                validar_fecha(fecha)
                self.fecha_caducidad = fecha
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_minimo_sugerido(self):
        """Edita el mínimo sugerido del reactivo."""
        while True:
            try:
                minimo_sugerido = obtener_float("\nMínimo sugerido: ")
                if minimo_sugerido < 0: raise Exception("El mínimo sugerido no puede ser negativo.")
                self.minimo_sugerido = minimo_sugerido
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_conversiones_posibles(self):
        """Edita las conversiones posibles del reactivo."""
        while True:
            try:
                print("\n1. Agregar conversión")
                print("2. Eliminar conversión")
                print("3. Continuar")
                match opcion():
                    case 1: self.agregar_conversion()
                    case 2: self.eliminar_conversion()
                    case 3: break
                    case _: raise Exception("Opción inválida. Intente de nuevo.")
            except Exception as e: print(f"\nError: {e}")

    def mostrar_conversiones(self):
        """Muestra las conversiones posibles del reactivo."""
        if self.conversiones_posibles:
            print("\nConversiones posibles:")
            for conversion in self.conversiones_posibles: print(conversion)
        else: print("No hay conversiones.")

    def agregar_conversion(self):
        """Agrega una conversión al reactivo."""
        while True:
            try:
                conversion = Conversion()
                conversion.editar()
                if conversion.unidad in [c.unidad for c in self.conversiones_posibles]: raise Exception("La conversión ya existe.")
                self.conversiones_posibles.append(conversion)
                print("\nConversión agregada exitosamente.")
                break
            except Exception as e: print(f"\nError: {e}")

    def eliminar_conversion(self):
        """Elimina una conversión del reactivo."""
        while True:
            try:
                if not self.conversiones_posibles:
                    print("\nNo hay conversiones.")
                    break
                self.mostrar_conversiones()
                unidad = obtener_float("\nUnidad de conversión a eliminar (vacío para volver): ")
                if not unidad: break
                self.conversiones_posibles = [c for c in self.conversiones_posibles if c.unidad != unidad]
                print("\nConversión eliminada exitosamente.")
                break
            except Exception as e: print(f"\nError: {e}")
    
    def obtener_conversion(self, unidad: str):
        """Obtiene una conversión."""
        return next((c for c in self.conversiones_posibles if c.unidad.lower() == unidad.lower()), None)