"Cada consulta tiene una fecha, hora, un objeto municipio y el nombre de la localidad consultada"

class Consulta:
    """Clase que representa una consulta de clima realizada por el usuario en la sesion."""

    def __init__(self, fecha, hora, municipio, localidad):
        self.fecha = fecha
        self.hora = hora
        self.municipio = municipio
        self.localidad = localidad