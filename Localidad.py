class Localidad:
    """Representa una localidad con coordenadas y consulta de clima."""

    def __init__(self, nombre, latitud, longitud):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.clima = None
    
    def cambiar_clima_actual(self, clima):
        """Cambia la información del clima de la localidad."""
        self.clima = clima    
        
    def mostrar_detalles(self):
        """Muestra la información de la localidad y su clima actual."""
        print(f"    Localidad: {self.nombre}")
        print(f"    Latitud: {self.latitud}")
        print(f"    Longitud: {self.longitud}")
        if self.clima:
            self.clima.mostrar_detalles()
        else:
            print("No hay información de clima disponible, realice la consulta en tiempo real.")
