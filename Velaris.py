
class Pasajero:
    def _init_(self, nombre, edad, sexo, clase, valor_del_tiquete, es_infante=False):
        if not nombre:
            raise ValueError("El nombre del pasajero no puede estar vacío.")
        
        try:
            edad = int(edad)
            if edad < 0:
                raise ValueError("La edad del pasajero no puede ser un número negativo.")
        except ValueError:
            raise ValueError(f"La edad del pasajero {nombre} debe ser un valor numérico.")
        
        if not clase:
            raise ValueError("La clase del pasajero no puede estar vacía.")
        
        try:
            valor_del_tiquete = float(valor_del_tiquete)
            if valor_del_tiquete < 0:
                raise ValueError("El precio del tiquete no puede ser un número negativo.")
        except ValueError:
            raise ValueError(f"El precio del tiquete del pasajero {nombre} debe ser un valor numérico.")
        
        self.nombre = nombre
        self.edad = edad
        self.sexo = sexo.lower()
        self.clase = clase.lower()
        self.valor_del_tiquete = valor_del_tiquete
        self.es_infante = es_infante or edad < 13
        self.cargas_especiales = []
        self.equipaje = 0
        
        if self.es_infante:
            self.valor_del_tiquete *= 0.93
            print(f"El pasajero {self.nombre} es un infante y se le aplicó el 7% de descuento. Valor final: {self.valor_del_tiquete:.2f}")

    def agregar_equipaje(self, peso):
        try:
            peso = float(peso)
            if peso < 0:
                raise ValueError("El peso del equipaje no puede ser negativo.")
            self.equipaje = peso
        except ValueError:
            raise ValueError("El peso del equipaje debe ser un valor numérico.")

    def agregar_carga_especial(self, carga):
        self.cargas_especiales.append(carga)

    def calcular_costo_equipaje(self):
        if self.clase == "economica":
            permitido = 10
            costo_extra = 5000
        elif self.clase == "ejecutiva":
            permitido = 20
            costo_extra = 10000
        elif self.clase == "premium":
            permitido = 30
            costo_extra = self.valor_del_tiquete * 0.01
        else:
            return 0
        
        if self.equipaje > permitido:
            return (self.equipaje - permitido) * costo_extra
        return 0

    def calcular_precio_final(self):
        precio_final = self.valor_del_tiquete
        precio_final += self.calcular_costo_equipaje()
        
        for carga in self.cargas_especiales:
            precio_final += carga.calculo_costo(self.valor_del_tiquete)
        
        return precio_final


class PasajeroEconomico(Pasajero):
    def _init_(self, nombre, edad, sexo, valor_del_tiquete):
        super()._init_(nombre, edad, sexo, "economica", valor_del_tiquete)


class PasajeroEjecutivo(Pasajero):
    def _init_(self, nombre, edad, sexo, valor_del_tiquete):
        super()._init_(nombre, edad, sexo, "ejecutiva", valor_del_tiquete)


class PasajeroPremium(Pasajero):
    def _init_(self, nombre, edad, sexo, valor_del_tiquete):
        super()._init_(nombre, edad, sexo, "premium", valor_del_tiquete)


class CargaEspecial:
    def _init_(self, tipo):
        self.tipo = tipo.lower()
        if not tipo:
            raise ValueError("El tipo de carga especial no puede estar vacío.")

    def calculo_costo(self, valor_tiquete):
        pass


class Bicicleta(CargaEspecial):
    def _init_(self, peso):
        super()._init_("bicicleta")
        try:
            self.peso = float(peso)
            if self.peso <= 0:
                raise ValueError("El peso no puede ser negativo o cero.")
        except ValueError:
            raise ValueError("El peso de la bicicleta debe ser un valor numérico.")

    def calculo_costo(self, valor_tiquete):
        return self.peso * 7000


class Mascota(CargaEspecial):
    def _init_(self, animal):
        super()._init_("mascota")
        self.animal = animal.lower()
        if self.animal not in ["perro", "gato"]:
            raise ValueError("Solo se permiten perros o gatos como mascotas.")

    def calculo_costo(self, valor_tiquete):
        if self.animal == "perro":
            return valor_tiquete * 0.05
        elif self.animal == "gato":
            return valor_tiquete * 0.02
        return 0


class Vuelo:
    def _init_(self, origen, destino):
        self.origen = origen
        self.destino = destino
        self.pasajeros = []
    
    def agregar_pasajero(self, pasajero):
        self.pasajeros.append(pasajero)
    
    def eliminar_pasajero(self, pasajero):
        if pasajero in self.pasajeros:
            self.pasajeros.remove(pasajero)
            return True
        return False
    
    def total_recaudado(self):
        return sum(p.calcular_precio_final() for p in self.pasajeros)
    
    def estadisticas_sexo(self):
        hombres = sum(1 for p in self.pasajeros if p.sexo == "masculino" or p.sexo == "hombre")
        mujeres = sum(1 for p in self.pasajeros if p.sexo == "femenino" or p.sexo == "mujer")
        return hombres, mujeres
    
    def promedio_tiquete(self):
        if not self.pasajeros:
            return 0
        return sum(p.valor_del_tiquete for p in self.pasajeros) / len(self.pasajeros)


class Aerolinea:
    def _init_(self, nombre):
        self.nombre = nombre
        self.vuelos = []
        self.total_recaudo_tiquetes = 0
        self.total_recaudo_equipaje = 0
    
    def crear_vuelo(self, origen, destino):
        vuelo = Vuelo(origen, destino)
        self.vuelos.append(vuelo)
        return vuelo
    
    def vender_tiquete(self, vuelo, pasajero):
        if vuelo not in self.vuelos:
            raise ValueError("El vuelo no existe en esta aerolínea.")
        
        vuelo.agregar_pasajero(pasajero)
        costo_total = pasajero.calcular_precio_final()
        self.total_recaudo_tiquetes += pasajero.valor_del_tiquete
        self.total_recaudo_equipaje += (costo_total - pasajero.valor_del_tiquete)
        
        print(f"Tiquete vendido a {pasajero.nombre} por ${costo_total:.2f}")
        return True
    
    def devolver_tiquete(self, vuelo, nombre_pasajero):
        for pasajero in vuelo.pasajeros:
            if pasajero.nombre == nombre_pasajero:
                costo_total = pasajero.calcular_precio_final()
                self.total_recaudo_tiquetes -= pasajero.valor_del_tiquete
                self.total_recaudo_equipaje -= (costo_total - pasajero.valor_del_tiquete)
                
                vuelo.eliminar_pasajero(pasajero)
                print(f"Tiquete de {nombre_pasajero} devuelto. Reembolso: ${costo_total:.2f}")
                return True
        print(f"No se encontró al pasajero {nombre_pasajero} en este vuelo.")
        return False
    
    def check_in(self, vuelo, nombre_pasajero):
        for pasajero in vuelo.pasajeros:
            if pasajero.nombre == nombre_pasajero:
                print(f"Check-in completado para {pasajero.nombre}")
                print(f"Equipaje: {pasajero.equipaje} kg")
                if pasajero.cargas_especiales:
                    print("Cargas especiales:")
                    for carga in pasajero.cargas_especiales:
                        print(f"- {carga.tipo}")
                costo_extra = pasajero.calcular_precio_final() - pasajero.valor_del_tiquete
                if costo_extra > 0:
                    print(f"Cargos adicionales: ${costo_extra:.2f}")
                return True
        print(f"No se encontró al pasajero {nombre_pasajero} en este vuelo.")
        return False
    
    def trayecto_mas_recaudado(self):
        if not self.vuelos:
            return None, 0
        
        max_recaudo = 0
        mejor_trayecto = None
        
        for vuelo in self.vuelos:
            recaudo = vuelo.total_recaudado()
            if recaudo > max_recaudo:
                max_recaudo = recaudo
                mejor_trayecto = (vuelo.origen, vuelo.destino)
        
        return mejor_trayecto, max_recaudo
    
    def estadisticas_por_destino(self, destino):
        vuelos_destino = [v for v in self.vuelos if v.destino.lower() == destino.lower()]
        if not vuelos_destino:
            return None
        
        total_hombres = 0
        total_mujeres = 0
        total_recaudo = 0
        total_pasajeros = 0
        
        for vuelo in vuelos_destino:
            h, m = vuelo.estadisticas_sexo()
            total_hombres += h
            total_mujeres += m
            total_recaudo += vuelo.total_recaudado()
            total_pasajeros += len(vuelo.pasajeros)
        
        promedio = total_recaudo / total_pasajeros if total_pasajeros > 0 else 0
        
        return {
            "hombres": total_hombres,
            "mujeres": total_mujeres,
            "total_recaudo": total_recaudo,
            "promedio_tiquete": promedio
        }


def mostrar_menu():
    print("\n=== MENÚ AEROLÍNEA ===")
    print("1. Crear vuelo")
    print("2. Vender tiquete")
    print("3. Hacer check-in")
    print("4. Devolver tiquete")
    print("5. Ver informaciòn adicional de trayectos")
    print("6. Salir del sistema")


def main():
    aerolinea = Aerolinea("VELARIS")
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            origen = input("Ingrese la ciudad de origen: ")
            destino = input("Ingrese la ciudad de destino: ")
            aerolinea.crear_vuelo(origen, destino)
            print(f"El vuelo fue creado a {origen} → {destino}")
        
        elif opcion == "2":
            if not aerolinea.vuelos:
                print("No hay vuelos disponibles, por favor cree un vuelo primero.")
                continue
                
            print("\n Los vuelos disponibles son: ")
            for i, vuelo in enumerate(aerolinea.vuelos, 1):
                print(f"{i}. {vuelo.origen} → {vuelo.destino}")
            
            try:
                seleccion = int(input("Seleccione el número del vuelo: ")) - 1
                if seleccion < 0 or seleccion >= len(aerolinea.vuelos):
                    raise ValueError
            except ValueError:
                print("La opciòn no es vàlida.")
                continue
                
            vuelo = aerolinea.vuelos[seleccion]
            
            nombre = input("Nombre del pasajero: ")
            edad = input("Edad: ")
            sexo = input("Sexo (hombre/mujer): ")
            clase = input("Clase (economica/ejecutiva/premium): ")
            valor_tiquete = input("Ingrese el valor del tiquete: ")
            
            try:
                if clase.lower() == "economica":
                    pasajero = PasajeroEconomico(nombre, edad, sexo, valor_tiquete)
                elif clase.lower() == "ejecutiva":
                    pasajero = PasajeroEjecutivo(nombre, edad, sexo, valor_tiquete)
                elif clase.lower() == "premium":
                    pasajero = PasajeroPremium(nombre, edad, sexo, valor_tiquete)
                else:
                    print("Clase no válida.")
                    continue
                
                equipaje = input("Ingrese el peso del equipaje (kg): ")
                pasajero.agregar_equipaje(equipaje)
                
                while True:
                    carga = input("¿Agregar carga especial? (bicicleta/mascota/ninguna): ").lower()
                    if carga == "ninguna":
                        break
                    elif carga == "bicicleta":
                        peso = input("Cuàl es el peso de la bicicleta (kg): ")
                        bicicleta = Bicicleta(peso)
                        pasajero.agregar_carga_especial(bicicleta)
                    elif carga == "mascota":
                        animal = input("Cuàl es el tipo de mascota (perro/gato): ")
                        mascota = Mascota(animal)
                        pasajero.agregar_carga_especial(mascota)
                    else:
                        print("La opción no es válida.")
                
                aerolinea.vender_tiquete(vuelo, pasajero)
                
            except ValueError as e:
                print(f"Error: {e}")
        
        elif opcion == "3":
            if not aerolinea.vuelos:
                print("No hay vuelos disponibles.")
                continue
                
            print("\n Los vuelos disponibles son: ")
            for i, vuelo in enumerate(aerolinea.vuelos, 1):
                print(f"{i}. {vuelo.origen} → {vuelo.destino}")
            
            try:
                seleccion = int(input("Seleccione el número del vuelo: ")) - 1
                if seleccion < 0 or seleccion >= len(aerolinea.vuelos):
                    raise ValueError
            except ValueError:
                print("La opciòn no es vàlida.")
                continue
                
            vuelo = aerolinea.vuelos[seleccion]
            nombre = input("Ingrese el nombre del pasajero: ")
            aerolinea.check_in(vuelo, nombre)
        
        elif opcion == "4":
            if not aerolinea.vuelos:
                print("No hay vuelos disponibles.")
                continue
                
            print("\n Los vuelos disponibles son: ")
            for i, vuelo in enumerate(aerolinea.vuelos, 1):
                print(f"{i}. {vuelo.origen} → {vuelo.destino}")
            
            try:
                seleccion = int(input("Seleccione el número del vuelo: ")) - 1
                if seleccion < 0 or seleccion >= len(aerolinea.vuelos):
                    raise ValueError
            except ValueError:
                print("La opciòn no es vàlida.")
                continue
                
            vuelo = aerolinea.vuelos[seleccion]
            nombre = input("Ingrese el nombre del pasajero: ")
            aerolinea.devolver_tiquete(vuelo, nombre)
        
        elif opcion == "5":
            print("\n Informaciòn adicional trayectos")
            
            trayecto, recaudo = aerolinea.trayecto_mas_recaudado()
            if trayecto:
                print(f"El trayecto más recaudado fue: {trayecto[0]} → {trayecto[1]} (${recaudo:.2f})")
            else:
                print("No hay vuelos con recaudo.")
            
           
            destino = input("Ingrese un destino para ver la informacìon (deje vacío para omitir): ")
            if destino:
                stats = aerolinea.estadisticas_por_destino(destino)
                if stats:
                    print(f"\n Informaciòn para {destino}:")
                    print(f"- Hombres: {stats['hombres']}")
                    print(f"- Mujeres: {stats['mujeres']}")
                    print(f"- El total recaudado fue: ${stats['total_recaudo']:.2f}")
                    print(f"- El precio promedio del tiquete fue de: ${stats['promedio_tiquete']:.2f}")
                else:
                    print(f"No se encontraron vuelos con destino a {destino}.")
            
            
            print("Total de la aerolínea VELARIS:")
            print(f"El recaudo por tiquetes es: ${aerolinea.total_recaudo_tiquetes:.2f}")
            print(f" El recaudo por equipaje y/o cargas es: ${aerolinea.total_recaudo_equipaje:.2f}")
            print(f"El recaudo total es: ${aerolinea.total_recaudo_tiquetes + aerolinea.total_recaudo_equipaje:.2f}")
        
        elif opcion == "6":
            print("Gracias por usar la aerolínea VELARIS. ¡Lo esperamos pronto!")
            break
        
        else:
            print("La opciòn no es válida, Por favor seleccione una opción del 1 al 6.")


if __name__ == "_main_":
    main()
    