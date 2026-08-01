from funciones import *
class Sistema:
    """ Clase principal que manejara el sistema y tendra todas las 
    opciones y requerimientos
    """    
    def __init__(self):
        self.nombres_municipios = [
            "Chacao"
            "Baruta"
            "El Hatillo"
            "Sucre"
            "Libertador"
        ]
        self.municipios = []

    def iniciar(self):
        """ Metodo que inicia el sistema
        """        
        # Carga aqui los municipios Jesus
        self.menu_principal()

    def menu_principal(self):
        """ Método que muestra el menu principal del sistema
        """        
        while True:
            titulo = "Menu principal MeteoCaracas"
            opciones = [
                "Buscar del clima en tiempo real",
                "Reportes y estadisticas",
                "Historicos"
            ]
            opcion = elegir_opcion(opciones, titulo, personalizado=True)
            if opcion == "0":
                print("Saliendo del sistema...")
                break
            if opcion == "1":
                self.menu_buscar_clima()
            if opcion == "2":
                self.reportes_estadisticas()
            if opcion == "3":
                self.historicos()

    def menu_buscar_clima(self):
        print("Menu buscar clima")
        pass
    
    def reportes_estadisticas(self):
        print("Menu reportes y estadisticas")
        pass

    def historicos(self):
        print("Menu historicos")
        pass