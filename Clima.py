class Clima:
    """Representa la información meteorológica obtenida para una localidad."""

    def __init__(self, temperatura, humedad, viento, codigo, estado):
        self.temperatura = temperatura
        self.humedad = humedad
        self.viento = viento
        self.codigo = codigo
        self.estado = estado

    def mostrar_detalles(self):
        print("\n       Detalles del clima")
        print(f"    Temperatura actual: {self.temperatura} °C")
        print(f"    Humedad relativa: {self.humedad} %")
        print(f"    Velocidad del viento: {self.viento} km/h")
        print(f"    Estado del tiempo: {self.estado}\n")
