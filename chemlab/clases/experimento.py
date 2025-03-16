from chemlab.utils import opcion, obtener_int, obtener_float, validar_fecha

class Experimento():

    def __init__(self, id, receta_id=0, personas_responsables: list[str]=[], fecha="", costo_asociado=1, resultado=""):
        self.id = id
        self.receta_id = receta_id
        self.personas_responsables = personas_responsables
        self.fecha = fecha
        self.costo_asociado = costo_asociado
        self.resultado = resultado

    def __str__(self):
        return  (f"\n--- Experimento {self.id} ---"
                f"\nID receta: {self.receta_id}"
                f"\nPersonas responsables: {self.obtener_personas_responsables()}"
                f"\nFecha: {self.fecha}"
                f"\nCosto asociado: {self.costo_asociado}"
                f"\nResultado: {self.resultado}")
    
    def obtener_personas_responsables(self): 
        if self.personas_responsables:
            personas = ""
            for i, persona in enumerate(self.personas_responsables): personas += f"\n{i + 1}. {persona}"
            return personas
        else: return "No hay personas responsables."
    
    def editar(self, db):
        while True:
            try:
                print(self)
                print("\n¿Qué desea editar?\n")
                print("1. ID receta")
                print("2. Personas responsables")
                print("3. Fecha")
                print("4. Costo asociado")
                print("5. Resultado")
                print("6. Volver")
                match opcion():
                    case 1: self.editar_receta_id(db)
                    case 2:
                        print("\nPersonas responsables: " + self.obtener_personas_responsables())
                        self.editar_personas_responsables()
                    case 3: self.editar_fecha()
                    case 4: self.editar_costo_asociado()
                    case 5: self.editar_resultado()
                    case 6: break
                    case _: raise Exception("Opción inválida. Intente de nuevo.")
                print("\nEdición exitosa.")
            except Exception as e: print(f"\nError: {e}")

    def editar_receta_id(self, db):
        while True:
            try:
                receta_id = obtener_int("\nID receta (vacío para volver): ")
                if not receta_id: return
                receta = next((receta for receta in db.recetas if receta.id == receta_id), None)
                if not receta: raise Exception("Receta no encontrada.")
                self.receta_id = receta_id
                return receta
            except Exception as e: print(f"\nError: {e}")
    
    def editar_personas_responsables(self):
        while True:
            try:
                print("\n¿Qué desea hacer?\n")
                print("1. Agregar persona responsable")
                print("2. Eliminar persona responsable")
                print("3. Continuar")
                match opcion():
                    case 1: self.agregar_persona_responsable()
                    case 2: self.eliminar_persona_responsable()
                    case 3: break
                    case _: raise Exception("Opción inválida. Intente de nuevo.")
            except Exception as e: print(f"\nError: {e}")

    def agregar_persona_responsable(self):
        while True:
            try:
                persona = input("\nPersona responsable (vacío para volver): ")
                if not persona: break
                self.personas_responsables.append(persona)
                print("\nPersona responsable agregada exitosamente.")
                break
            except Exception as e: print(f"\nError: {e}")

    def eliminar_persona_responsable(self):
        while True:
            try:
                if not self.personas_responsables:
                    print("\nNo hay personas responsables.")
                    break
                num = obtener_int("\nNúmero de persona responsable a eliminar: ")
                if num < 1 or num > len(self.personas_responsables): raise Exception("Número inválido.")
                self.personas_responsables.pop(num - 1)
                print("\nPersona responsable eliminada exitosamente.")
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_fecha(self):
        while True:
            try:
                fecha = input("\nFecha (YYYY-MM-DD): ")
                if not fecha:
                    self.fecha_caducidad = ""
                    break
                validar_fecha(fecha)
                self.fecha_caducidad = fecha
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_costo_asociado(self):
        while True:
            try:
                costo_asociado = obtener_float("\nCosto asociado: ")
                if not costo_asociado:
                    self.costo_asociado = 0
                    break
                if costo_asociado < 0: raise Exception("El costo asociado no puede ser negativo.")
                self.costo_asociado = costo_asociado
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_resultado(self):
        while True:
            try:
                resultado = input("\nResultado: ")
                if not resultado: raise Exception("El resultado no puede estar vacío.")
                self.resultado = resultado
                break
            except Exception as e: print(f"\nError: {e}")