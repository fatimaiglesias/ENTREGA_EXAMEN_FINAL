from abc import ABC, abstractmethod
import json

class Persona:
    def __init__(self, nombre, email):
        self.nombre = nombre
        self.email = email

class Comprador(Persona):
    def __init__(self, nombre, email):
        super().__init__(nombre, email)

class Organizador(Persona):
    def __init__(self, nombre, email):
        super().__init__(nombre, email)

class Evento(ABC):
    @abstractmethod
    def mostrar_detalle(self):
        pass

class EventoParrillada(Evento):
    def __init__(self, nombre, fecha, lugar, precio):
        self.nombre = nombre
        self.fecha = fecha
        self.lugar = lugar
        self.precio = precio

    def mostrar_detalle(self):
        print(f"Evento de Parrillada: {self.nombre}")
        print(f"Fecha: {self.fecha}")
        print(f"Lugar: {self.lugar}")
        print(f"Precio: ${self.precio}")

class EventoVIP(Evento):
    def __init__(self, nombre, fecha, lugar, precio, beneficios):
        self.nombre = nombre
        self.fecha = fecha
        self.lugar = lugar
        self.precio = precio
        self.beneficios = beneficios

    def mostrar_detalle(self):
        print(f"Evento VIP: {self.nombre}")
        print(f"Fecha: {self.fecha}")
        print(f"Lugar: {self.lugar}")
        print(f"Precio: ${self.precio}")
        print("Beneficios adicionales:")
        for beneficio in self.beneficios:
            print(f"- {beneficio}")

class Venta:
    def __init__(self, comprador, evento, cantidad):
        self.comprador = comprador
        self.evento = evento
        self.cantidad = cantidad

    def calcular_descuento(self):
        descuento = 0
        if isinstance(self.evento, EventoVIP):
            descuento += 0.1 * self.cantidad  
        if self.cantidad >= 5:
            descuento += 0.05 * self.cantidad  
        return descuento

    def calcular_total(self):
        subtotal = self.cantidad * self.evento.precio
        descuento = self.calcular_descuento()
        total = subtotal - descuento
        return total

class GestorVentas:
    def __init__(self):
        self.ventas = []

    def agregar_venta(self, venta):
        self.ventas.append(venta)

    def generar_reporte_ventas(self):
        reporte = {}
        for venta in self.ventas:
            evento_nombre = venta.evento.nombre
            if evento_nombre not in reporte:
                reporte[evento_nombre] = {
                    'total_ventas': 0,
                    'total_dinero': 0
                }
            reporte[evento_nombre]['total_ventas'] += venta.cantidad
            reporte[evento_nombre]['total_dinero'] += venta.calcular_total()
        return reporte

    def cargar_ventas_desde_json(self, archivo):
        with open(archivo, 'r') as file:
            datos_ventas = json.load(file)
            for venta_data in datos_ventas:
                comprador = Comprador(venta_data['comprador']['nombre'], venta_data['comprador']['email'])
                evento_data = venta_data['evento']
                evento = EventoVIP(evento_data['nombre'], evento_data['fecha'], evento_data['lugar'], evento_data['precio'], evento_data['beneficios']) if 'beneficios' in evento_data else EventoParrillada(evento_data['nombre'], evento_data['fecha'], evento_data['lugar'], evento_data['precio'])
                venta = Venta(comprador, evento, venta_data['cantidad'])
                self.agregar_venta(venta)

    def guardar_ventas_a_json(self, archivo):
        datos_ventas = []
        for venta in self.ventas:
            venta_data = {
                'comprador': {
                    'nombre': venta.comprador.nombre,
                    'email': venta.comprador.email
                },
                'evento': {
                    'nombre': venta.evento.nombre,
                    'fecha': venta.evento.fecha,
                    'lugar': venta.evento.lugar,
                    'precio': venta.evento.precio
                },
                'cantidad': venta.cantidad
            }
            if isinstance(venta.evento, EventoVIP):
                venta_data['evento']['beneficios'] = venta.evento.beneficios
            datos_ventas.append(venta_data)
        with open(archivo, 'w') as file:
            json.dump(datos_ventas, file, indent=4)

class EventoAgotadoError(Exception):
    def __init__(self, evento_nombre):
        super().__init__(f"El evento '{evento_nombre}' está agotado.")

class DatosInvalidosError(Exception):
    def __init__(self, mensaje):
        super().__init__(f"Datos inválidos: {mensaje}")

class CargaArchivoError(Exception):
    def __init__(self, archivo, mensaje):
        super().__init__(f"Error al cargar el archivo '{archivo}': {mensaje}")

class GuardadoArchivoError(Exception):
    def __init__(self, archivo, mensaje):
        super().__init__(f"Error al guardar el archivo '{archivo}': {mensaje}")

def mostrar_menu_eventos():
    print("Seleccione un evento:")
    print("1. Parrillada  - $25")
    print("2. Evento VIP - $50")
    opcion = input("Ingrese el número de su elección: ")
    return opcion

def obtener_evento(opcion):
    if opcion == '1':
        return EventoParrillada("Parrillada ", "2024-06-20", "Parque Central", 25)
    elif opcion == '2':
        return EventoVIP("Evento VIP ", "2024-07-15", "Salón Principal", 50, ["Asientos VIP", "Catering exclusivo"])
    else:
        raise DatosInvalidosError("La opción seleccionada no es válida.")

def main():
    try:
        gestor_ventas = GestorVentas()
        
        while True:
            opcion_evento = mostrar_menu_eventos()
            evento_seleccionado = obtener_evento(opcion_evento)
            
            cantidad_tickets = int(input("Ingrese la cantidad de tickets que desea comprar: "))
            comprador_nombre = input("Ingrese su nombre: ")
            comprador_email = input("Ingrese su email: ")
            comprador = Comprador(comprador_nombre, comprador_email)
            
            venta = Venta(comprador, evento_seleccionado, cantidad_tickets)
            gestor_ventas.agregar_venta(venta)
            
            continuar = input("¿Desea agregar otra venta? (s/n): ")
            if continuar.lower() != 's':
                break
        
        reporte_ventas = gestor_ventas.generar_reporte_ventas()
        print("\nReporte de Ventas:")
        for evento, datos in reporte_ventas.items():
            print(f"Evento: {evento}")
            print(f"Total Ventas: {datos['total_ventas']}")
            print(f"Total Dinero: ${datos['total_dinero']}")
            print()
        
        gestor_ventas.guardar_ventas_a_json('ventas.json')
        print("¡Ventas guardadas exitosamente!")

    except (DatosInvalidosError, ValueError) as e:
        print("Error:", e)
    except (EventoAgotadoError, CargaArchivoError, GuardadoArchivoError) as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
