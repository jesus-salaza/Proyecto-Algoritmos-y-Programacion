from Municipio import Municipio

class Consulta:
    """Clase que representa una consulta de clima realizada por el usuario en la sesion."""

    def __init__(self, fecha, hora, municipio, posicion_localidad):
        self.fecha = fecha
        #self.hora = hora
        self.municipio = municipio
        self.posicion_localidad = posicion_localidad
        
    def mostrar_detalles(self, sistema):
        """Muestra los detalles de la consulta, incluyendo la fecha, hora, municipio y localidad."""
        print(f"\nConsulta realizada el {self.fecha} a las {self.hora}")
        self.municipio.mostrar_detalles(self.posicion_localidad)