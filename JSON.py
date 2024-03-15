import json

# Crear datos de ventas para el ejemplo
ventas = [
    {
        "comprador": {
            "nombre": "Juan Perez",
            "email": "juan@example.com"
        },
        "evento": {
            "nombre": "Parrillada de Verano",
            "fecha": "2024-06-20",
            "lugar": "Parque Central",
            "precio": 25
        },
        "cantidad": 3
    },
    {
        "comprador": {
            "nombre": "María González",
            "email": "maria@example.com"
        },
        "evento": {
            "nombre": "Evento VIP de Barbacoa",
            "fecha": "2024-07-15",
            "lugar": "Salón Principal",
            "precio": 50,
            "beneficios": ["Asientos VIP", "Catering exclusivo"]
        },
        "cantidad": 2
    }
]


with open('ventas.json', 'w') as file:
    json.dump(ventas, file, indent=4)
