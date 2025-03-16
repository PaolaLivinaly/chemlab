from chemlab.clases.reactivo_utilizado import ReactivoUtilizado
from chemlab.clases.valor_a_medir import ValorAMedir
from chemlab.utils import opcion, obtener_int

class Receta():
    def __init__(self, id, nombre="Receta Genérica", objetivo="Objetivo Genérico", reactivos_utilizados: list[ReactivoUtilizado]=[], procedimiento: list[str]=[], valores_a_medir: list[ValorAMedir]=[]):
        self.id = id
        self.nombre = nombre
        self.objetivo = objetivo
        self.reactivos_utilizados = reactivos_utilizados
        self.procedimiento = procedimiento
        self.valores_a_medir = valores_a_medir

    def __str__(self):
        return  (f"\n--- Receta {self.id} ---"
                f"\nNombre: {self.nombre}"
                f"\nObjetivo: {self.objetivo}"
                f"\nReactivos utilizados: {self.obtener_reactivos_utilizados()}"
                f"\nProcedimiento: {self.obtener_procedimiento()}"
                f"\nValores a medir: {self.obtener_valores_a_medir()}")
    
    def obtener_reactivos_utilizados(self):
        if self.reactivos_utilizados:
            reactivos = ""
            for reactivo in self.reactivos_utilizados: reactivos += f"\n- {reactivo}"
            return reactivos
        else: return "No hay reactivos utilizados."

    def obtener_procedimiento(self):
        if self.procedimiento:
            procedimiento = ""
            for i, paso in enumerate(self.procedimiento): procedimiento += f"\n{i + 1}. {paso}"
            return procedimiento
        else: return "No hay procedimiento."

    def obtener_valores_a_medir(self):
        if self.valores_a_medir:
            valores = ""
            for i, valor in enumerate(self.valores_a_medir): valores += f"\n{i + 1}. {valor}"
            return valores
        else: return "No hay valores a medir."

    def obtener_reactivo_utilizado_por_id(self, reactivo_id): return next((reactivo for reactivo in self.reactivos_utilizados if reactivo.reactivo_id == reactivo_id), None)
    
    def editar(self, db):
        while True:
            try:
                print(self)
                print("\n¿Qué desea editar?\n")
                print("1. Nombre")
                print("2. Objetivo")
                print("3. Reactivos utilizados")
                print("4. Procedimiento")
                print("5. Valores a medir")
                print("6. Volver")
                match opcion():
                    case 1: self.editar_nombre()
                    case 2: self.editar_objetivo()
                    case 3: self.editar_reactivos_utilizados(db)
                    case 4: self.editar_procedimiento()
                    case 5: self.editar_valores_a_medir()
                    case 6: break
                    case _: raise Exception("Opción inválida. Intente de nuevo.")
                print("\nEdición exitosa.")
            except Exception as e: print(f"\nError: {e}")

    def editar_nombre(self):
        while True:
            try:
                nombre = input("\nNombre: ")
                if not nombre: raise Exception("El nombre no puede estar vacío.")
                self.nombre = nombre
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_objetivo(self):
        while True:
            try:
                objetivo = input("\nObjetivo: ")
                if not objetivo: raise Exception("El objetivo no puede estar vacío.")
                self.objetivo = objetivo
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_reactivos_utilizados(self, db):
        while True:
            try:
                print("\nReactivos utilizados: " + self.obtener_reactivos_utilizados())
                print("\n¿Qué desea hacer?\n")
                print("1. Agregar reactivo utilizado")
                print("2. Eliminar reactivo utilizado")
                print("3. Continuar")
                match opcion():
                    case 1: self.agregar_reactivo_utilizado(db)
                    case 2: self.eliminar_reactivo_utilizado(db)
                    case 3: break
                    case _: raise Exception("Opción inválida. Intente de nuevo.")
            except Exception as e: print(f"\nError: {e}")

    def agregar_reactivo_utilizado(self, db):
        while True:
            try:
                reactivo_id = obtener_int("\nID reactivo (vacío para volver): ")
                if not reactivo_id: break
                if any(reactivo.reactivo_id == reactivo_id for reactivo in self.reactivos_utilizados): raise Exception("El reactivo ya está en la lista.")
                if not any(reactivo.id == reactivo_id for reactivo in db.reactivos): raise Exception("El reactivo no existe.")
                reactivo_utilizado = ReactivoUtilizado(reactivo_id)
                reactivo_utilizado.editar_cantidad_necesaria()
                reactivo_utilizado.editar_unidad_medida()
                self.reactivos_utilizados.append(reactivo_utilizado)
                print("\nReactivo utilizado agregado exitosamente.")
                break
            except Exception as e: print(f"\nError: {e}")

    def eliminar_reactivo_utilizado(self):
        while True:
            try:
                if not self.reactivos_utilizados:
                    print("\nNo hay reactivos utilizados.")
                    break
                reactivo_id = obtener_int("\nID reactivo (vacío para volver): ")
                if not reactivo_id: break
                reactivo_utilizado = self.obtener_reactivo_utilizado_por_id(reactivo_id)
                if not reactivo_utilizado: raise Exception("El reactivo no está en la lista.")
                self.reactivos_utilizados.remove(reactivo_utilizado)
                print("\nReactivo utilizado eliminado exitosamente.")
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_procedimiento(self):
        while True:
            try:
                print("\nProcedimiento: " + self.obtener_procedimiento())
                print("\n¿Qué desea hacer?\n")
                print("1. Agregar paso")
                print("2. Eliminar paso")
                print("3. Eliminar todos los pasos")
                print("4. Continuar")
                match opcion():
                    case 1: self.agregar_paso()
                    case 2: self.eliminar_paso()
                    case 3:
                        self.procedimiento.clear()
                        print("\nTodos los pasos han sido eliminados.")
                    case 4: break
                    case _: raise Exception("Opción inválida. Intente de nuevo.")
            except Exception as e: print(f"\nError: {e}")

    def agregar_paso(self):
        while True:
            try:
                paso = input("\nPaso (vacío para volver): ")
                if not paso: break
                posicion = obtener_int("\nPosición (vacío para agregar al final): ")
                if not posicion: self.procedimiento.append(paso)
                else: self.procedimiento.insert(posicion - 1, paso)
                print("\nPaso agregado exitosamente.")
                break
            except Exception as e: print(f"\nError: {e}")

    def eliminar_paso(self):
        while True:
            try:
                if not self.procedimiento:
                    print("\nNo hay pasos.")
                    break
                num = obtener_int("\nNúmero de paso a eliminar: ")
                if num < 1 or num > len(self.procedimiento): raise Exception("Número inválido.")
                self.procedimiento.pop(num - 1)
                print("\nPaso eliminado exitosamente.")
                break
            except Exception as e: print(f"\nError: {e}")

    def editar_valores_a_medir(self):
        while True:
            try:
                print("\nValores a medir: " + self.obtener_valores_a_medir())
                print("\n¿Qué desea hacer?\n")
                print("1. Agregar valor a medir")
                print("2. Eliminar valor a medir")
                print("3. Eliminar todos los valores a medir")
                print("4. Continuar")
                match opcion():
                    case 1: self.agregar_valor_a_medir()
                    case 2: self.eliminar_valor_a_medir()
                    case 3:
                        self.valores_a_medir.clear()
                        print("\nTodos los valores a medir han sido eliminados.")
                    case 4: break
                    case _: raise Exception("Opción inválida. Intente de nuevo.")
            except Exception as e: print(f"\nError: {e}")

    def agregar_valor_a_medir(self):
        while True:
            try:
                valor = ValorAMedir()
                valor.editar_nombre()
                valor.editar_formula()
                valor.editar_minimo()
                valor.editar_maximo()
                self.valores_a_medir.append(valor)
                print("\nValor a medir agregado exitosamente.")
                break
            except Exception as e: print(f"\nError: {e}")

    def eliminar_valor_a_medir(self):
        while True:
            try:
                if not self.valores_a_medir:
                    print("\nNo hay valores a medir.")
                    break
                num = obtener_int("\nNúmero de valor a medir a eliminar: ")
                if num < 1 or num > len(self.valores_a_medir): raise Exception("Número inválido.")
                self.valores_a_medir.pop(num - 1)
                print("\nValor a medir eliminado exitosamente.")
                break
            except Exception as e: print(f"\nError: {e}")