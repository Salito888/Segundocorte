
from abc import ABC, abstractmethod

class Pasajero(ABC):
    def _init_(self, nombre, edad, sexo, valor_del_tiquete):
        self._nombre = self._validar_nombre(nombre)
        self._edad = self._validar_edad(edad)
        self._sexo = self._validar_sexo(sexo)
        self._valor_del_tiquete = self._validar_valor_tiquete(valor_del_tiquete)
        self._es_infante = self._edad < 13
        self._cargas_especiales = []
        self._equipaje = 0
        
        if self._es_infante:
            self._aplicar_descuento_infante()

    @property
    def nombre(self):
        return self._nombre
    
    @property
    def edad(self):
        return self._edad
    
    @property
    def sexo(self):
        return self._sexo
    
    @property
    def valor_del_tiquete(self):
        return self._valor_del_tiquete
    
    @property
    def es_infante(self):
        return self._es_infante
    
    @property
    def equipaje(self):
        return self._equipaje
    
    @property
    def cargas_especiales(self):
        return self._cargas_especiales
    
    @property
    @abstractmethod
    def clase(self):
        pass

    def _validar_nombre(self, nombre):
        if not nombre:
            raise ValueError("El nombre del pasajero no puede estar vacío.")
        return nombre

    def _validar_edad(self, edad):
        try:
            edad = int(edad)
            if edad < 0:
                raise ValueError("La edad del pasajero no puede ser un número negativo.")
            return edad
        except ValueError:
            raise ValueError(f"La edad del pasajero {self._nombre} debe ser un valor numérico.")

    def _validar_sexo(self, sexo):
        sexo = sexo.lower()
        if sexo not in ["masculino", "femenino", "hombre", "mujer"]:
            raise ValueError("Sexo debe ser 'masculino' o 'femenino'")
        return sexo

    def _validar_valor_tiquete(self, valor):
        try:
            valor = float(valor)
            if valor < 0:
                raise ValueError("El precio del tiquete no puede ser un número negativo.")
            return valor
        except ValueError:
            raise ValueError(f"El precio del tiquete del pasajero {self._nombre} debe ser un valor numérico.")

    def _aplicar_descuento_infante(self):
        descuento = 0.07
        self._valor_del_tiquete *= (1 - descuento)
        print(f"El pasajero {self._nombre} es un infante y se le aplicó el {descuento*100:.0f}% de descuento. Valor final: {self._valor_del_tiquete:.2f}")

    def agregar_equipaje(self, peso):
        try:
            peso = float(peso)
            if peso < 0:
                raise ValueError("El peso del equipaje no puede ser negativo.")
            self._equipaje = peso
        except ValueError:
            raise ValueError("El peso del equipaje debe ser un valor numérico.")

    def agregar_carga_especial(self, carga):
        if not isinstance(carga, CargaEspecial):
            raise ValueError("La carga debe ser una instancia de CargaEspecial")
        self._cargas_especiales.append(carga)

    @abstractmethod
    def calcular_costo_equipaje(self):
        pass

    def calcular_precio_final(self):
        precio_final = self._valor_del_tiquete
        precio_final += self.calcular_costo_equipaje()
        
        for carga in self._cargas_especiales:
            precio_final += carga.calculo_costo(self._valor_del_tiquete)
        
        return precio_final


class PasajeroEconomico(Pasajero):
    @property
    def clase(self):
        return "economica"
    
    def calcular_costo_equipaje(self):
        permitido = 10
        costo_extra = 5000
        
        if self.equipaje > permitido:
            return (self.equipaje - permitido) * costo_extra
        return 0


class PasajeroEjecutivo(Pasajero):
    @property
    def clase(self):
        return "ejecutiva"
    
    def calcular_costo_equipaje(self):
        permitido = 20
        costo_extra = 10000
        
        if self.equipaje > permitido:
            return (self.equipaje - permitido) * costo_extra
        return 0


class PasajeroPremium(Pasajero):
    @property
    def clase(self):
        return "premium"
    
    def calcular_costo_equipaje(self):
        permitido = 30
        costo_extra = self.valor_del_tiquete * 0.01
        
        if self.equipaje > permitido:
            return (self.equipaje - permitido) * costo_extra
        return 0


class CargaEspecial(ABC):
    def _init_(self, tipo):
        self._tipo = tipo.lower()
        if not tipo:
            raise ValueError("El tipo de carga especial no puede estar vacío.")
    
    @property
    def tipo(self):
        return self._tipo
    
    @abstractmethod
    def calculo_costo(self, valor_tiquete):
        pass


class Bicicleta(CargaEspecial):
    def _init_(self, peso):
        super()._init_("bicicleta")
        self._peso = self._validar_peso(peso)
    
    @property
    def peso(self):
        return self._peso
    
    def _validar_peso(self, peso):
        try:
            peso = float(peso)
            if peso <= 0:
                raise ValueError("El peso no puede ser negativo o cero.")
            return peso
        except ValueError:
            raise ValueError("El peso de la bicicleta debe ser un valor numérico.")

    def calculo_costo(self, valor_tiquete):
        return self._peso * 7000


class Mascota(CargaEspecial):
    def _init_(self, animal):
        super()._init_("mascota")
        self._animal = self._validar_animal(animal)
    
    @property
    def animal(self):
        return self._animal
    
    def _validar_animal(self, animal):
        animal = animal.lower()
        if animal not in ["perro", "gato"]:
            raise ValueError("Solo se permiten perros o gatos como mascotas.")
        return animal

    def calculo_costo(self, valor_tiquete):
        if self._animal == "perro":
            return valor_tiquete * 0.05
        elif self._animal == "gato":
            return valor_tiquete * 0.02
        return 0


class Vuelo:
    def _init_(self, origen, destino):
        self._origen = origen
        self._destino = destino
        self._pasajeros = []
    
    @property
    def origen(self):
        return self._origen
    
    @property
    def destino(self):
        return self._destino
    
    @property
    def pasajeros(self):
        return self._pasajeros
    
    def agregar_pasajero(self, pasajero):
        self._pasajeros.append(pasajero)
    
    def eliminar_pasajero(self, pasajero):
        if pasajero in self._pasajeros:
            self._pasajeros.remove(pasajero)
            return True
        return False
    
    def total_recaudado(self):
        return sum(p.calcular_precio_final() for p in self._pasajeros)
    
    def estadisticas_sexo(self):
        hombres = sum(1 for p in self._pasajeros if p.sexo in ["masculino", "hombre"])
        mujeres = sum(1 for p in self._pasajeros if p.sexo in ["femenino", "mujer"])
        return hombres, mujeres
    
    def promedio_tiquete(self):
        if not self._pasajeros:
            return 0
        return sum(p.valor_del_tiquete for p in self._pasajeros) / len(self._pasajeros)


class Aerolinea:
    def _init_(self, nombre):
        self._nombre = nombre
        self._vuelos = []
        self._total_recaudo_tiquetes = 0
        self._total_recaudo_equipaje = 0
    
    @property
    def nombre(self):
        return self._nombre
    
    @property
    def vuelos(self):
        return self._vuelos
    
    @property
    def total_recaudo_tiquetes(self):
        return self._total_recaudo_tiquetes
    
    @property
    def total_recaudo_equipaje(self):
        return self._total_recaudo_equipaje
    
    def crear_vuelo(self, origen, destino):
        vuelo = Vuelo(origen, destino)
        self._vuelos.append(vuelo)
        return vuelo
    
    def vender_tiquete(self, vuelo, pasajero):
        if vuelo not in self._vuelos:
            raise ValueError("El vuelo no existe en esta aerolínea.")
        
        vuelo.agregar_pasajero(pasajero)
        costo_total = pasajero.calcular_precio_final()
        self._total_recaudo_tiquetes += pasajero.valor_del_tiquete
        self._total_recaudo_equipaje += (costo_total - pasajero.valor_del_tiquete)
        
        print(f"Tiquete vendido a {pasajero.nombre} por ${costo_total:.2f}")
        return True
    
    def devolver_tiquete(self, vuelo, nombre_pasajero):
        for pasajero in vuelo.pasajeros:
            if pasajero.nombre == nombre_pasajero:
                costo_total = pasajero.calcular_precio_final()
                self._total_recaudo_tiquetes -= pasajero.valor_del_tiquete
                self._total_recaudo_equipaje -= (costo_total - pasajero.valor_del_tiquete)
                
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
        if not self._vuelos:
            return None, 0
        
        max_recaudo = 0
        mejor_trayecto = None
        
        for vuelo in self._vuelos:
            recaudo = vuelo.total_recaudado()
            if recaudo > max_recaudo:
                max_recaudo = recaudo
                mejor_trayecto = (vuelo.origen, vuelo.destino)
        
        return mejor_trayecto, max_recaudo
    
    def estadisticas_por_destino(self, destino):
        vuelos_destino = [v for v in self._vuelos if v.destino.lower() == destino.lower()]
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
    print("MENÚ AEROLÍNEA VELARIS")
    print("1. Crear vuelo")
    print("2. Vender tiquete")
    print("3. Hacer check-in")
    print("4. Devolver tiquete")
    print("5. Ver informaciòn de trayectos")
    print("6. Salir")


def main():
    aerolinea = Aerolinea()
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            origen = input("Ingrese la ciudad de origen: ")
            destino = input("Ingrese la ciudad de destino: ")
            aerolinea.crear_vuelo(origen, destino)
            print(f"Vuelo creado: {origen} → {destino}")
        
        elif opcion == "2":
            if not aerolinea.vuelos:
                print("No hay vuelos disponibles. Cree un vuelo primero.")
                continue
                
            print("\nVuelos disponibles:")
            for i, vuelo in enumerate(aerolinea.vuelos, 1):
                print(f"{i}. {vuelo.origen} → {vuelo.destino}")
            
            try:
                seleccion = int(input("Seleccione el número del vuelo: ")) - 1
                if seleccion < 0 or seleccion >= len(aerolinea.vuelos):
                    raise ValueError
            except ValueError:
                print("La selección no fue válida.")
                continue
                
            vuelo = aerolinea.vuelos[seleccion]
            
            nombre = input("Ingrese el nombre del pasajero: ")
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
                    print("La clase no fue válida.")
                    continue
                
                equipaje = input("Ingrese el peso del equipaje (kg): ")
                pasajero.agregar_equipaje(equipaje)
                
                while True:
                    carga = input("¿Desea agregar carga especial? (bicicleta/mascota/ninguna): ").lower()
                    if carga == "ninguna":
                        break
                    elif carga == "bicicleta":
                        peso = input("Ingrese el peso de la bicicleta (kg): ")
                        bicicleta = Bicicleta(peso)
                        pasajero.agregar_carga_especial(bicicleta)
                    elif carga == "mascota":
                        animal = input("Ingrese el tipo de mascota (perro/gato): ")
                        mascota = Mascota(animal)
                        pasajero.agregar_carga_especial(mascota)
                    else:
                        print("Opción no válida.")
                
                aerolinea.vender_tiquete(vuelo, pasajero)
                
            except ValueError as e:
                print(f"Error: {e}")
        
        elif opcion == "3":
            if not aerolinea.vuelos:
                print("No hay vuelos disponibles.")
                continue
                
            print("Vuelos disponibles: ")
            for i, vuelo in enumerate(aerolinea.vuelos, 1):
                print(f"{i}. {vuelo.origen} → {vuelo.destino}")
            
            try:
                seleccion = int(input("Seleccione el número del vuelo: ")) - 1
                if seleccion < 0 or seleccion >= len(aerolinea.vuelos):
                    raise ValueError
            except ValueError:
                print("La selección no fue válida.")
                continue
                
            vuelo = aerolinea.vuelos[seleccion]
            nombre = input("Ingrese el nombre del pasajero: ")
            aerolinea.check_in(vuelo, nombre)
        
        elif opcion == "4":
            if not aerolinea.vuelos:
                print("No hay vuelos disponibles.")
                continue
                
            print("Vuelos disponibles:")
            for i, vuelo in enumerate(aerolinea.vuelos, 1):
                print(f"{i}. {vuelo.origen} → {vuelo.destino}")
            
            try:
                seleccion = int(input("Seleccione el número del vuelo: ")) - 1
                if seleccion < 0 or seleccion >= len(aerolinea.vuelos):
                    raise ValueError
            except ValueError:
                print("La selección no fue válida.")
                continue
                
            vuelo = aerolinea.vuelos[seleccion]
            nombre = input("Ingrese el nombre del pasajero: ")
            aerolinea.devolver_tiquete(vuelo, nombre)
        
        elif opcion == "5":
            print(" Informaciòn adicional")
            
            trayecto, recaudo = aerolinea.trayecto_mas_recaudado()
            if trayecto:
                print(f"Trayecto más recaudado: {trayecto[0]} → {trayecto[1]} (${recaudo:.2f})")
            else:
                print("No hay vuelos con recaudo.")
            
            
            destino = input("Ingrese un destino para ver toda la informaciòn (deje vacío para omitir): ")
            if destino:
                stats = aerolinea.estadisticas_por_destino(destino)
                if stats:
                    print(f"Informaciòn para {destino}:")
                    print(f"- Hombres: {stats['hombres']}")
                    print(f"- Mujeres: {stats['mujeres']}")
                    print(f"- El total recaudado es: ${stats['total_recaudo']:.2f}")
                    print(f"- El precio promedio del tiquete es: ${stats['promedio_tiquete']:.2f}")
                else:
                    print(f"No se encontraron vuelos con destino a {destino}.")
            
           
            print("Totales de la aerolínea VELARIS:")
            print(f"- Recaudo por tiquetes: ${aerolinea.total_recaudo_tiquetes:.2f}")
            print(f"- Recaudo por equipaje/cargas: ${aerolinea.total_recaudo_equipaje:.2f}")
            print(f"- Recaudo total: ${aerolinea.total_recaudo_tiquetes + aerolinea.total_recaudo_equipaje:.2f}")
        
        elif opcion == "6":
            print("Gracias por usar la aerolínea VELARIS. ¡lo esperamos pronto!")
            break
        
        else:
            print("La opción no es válida. Por favor seleccione una opción del 1 al 6.")


if __name__ == "__main__":
    main()



    

