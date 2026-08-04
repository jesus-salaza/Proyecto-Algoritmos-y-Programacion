from Municipio import Municipio
from Localidad import Localidad
from funciones import *
import json
class Sistema:
    """ Clase principal que manejara el sistema y tendra todas las 
    opciones y requerimientos
    """    
    def __init__(self):
        self.nombres_municipios = []
        self.municipios = []
        self.consultas = []

    def cargar_municipios(self, nombre_json_municipios):
        """ Metodo que carga los municipios del json
        """
        
        with open(nombre_json_municipios, "r", encoding="utf-8") as archivo:
            data = json.load(archivo)

        lista_llaves = list(data.keys())
        
        for nombre_municipio in lista_llaves:
            municipio = Municipio(nombre_municipio)
            
            for localidad in data[nombre_municipio]:
                
                nombre_localidad = localidad["localidad"]
                latitud = localidad["latitud"]
                longitud = localidad["longitud"]
                nueva_localidad = Localidad(nombre_localidad, latitud, longitud)
                
                municipio.agregar_localidad(nueva_localidad)
            
            self.nombres_municipios.append(nombre_municipio)
            self.municipios.append(municipio)
            
        print("Municipios cargados correctamente")
            
    def iniciar(self,nombre_json_municipios):
        """ Metodo que inicia el sistema
        """        
        self.cargar_municipios(nombre_json_municipios)
        self.menu_principal()

    def menu_principal(self):
        """ Método que muestra el menu principal del sistema
        """        
        while True:
            
            print(' ---------- MENU PRINCIPAL METEOCARACAS ----------"\n')
            opciones = [
                "Consulta del clima en tiempo real",
                "Reportes y estadisticas",
                "Historicos"
            ]
            opcion = elegir_opcion(opciones)
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
        while True:
            titulo = "Consulta del clima en tiempo real"
            opciones = [
                        "Buscar por municipio y localidad",
                        "Buscar por nombre de la localidad",
                    ]
            opcion = elegir_opcion(opciones, titulo, True)
            if opcion == "0":
                print("Saliendo al menu pricipal...")
                break
            if opcion == "1": # Buscar por municipio y localidad
                while True:
                    
                    titulo = "Buscar por municipio y localidad"
                    n_municipio = elegir_opcion(self.municipios, titulo)
                    if n_municipio == "0":
                        print("Saliendo al menu de consulta del clima")
                        break
                    elegido = self.municipios[int(n_municipio)-1]
                    
                    titulo = "Seleccione la localidad"
                    localidades_disponibles = []
                    for localidad in elegido.localidades:
                        localidades_disponibles.append(localidad.nombre)  # Lo reviso luego, SIRVE
                    n_localidad = elegir_opcion(localidades_disponibles, titulo)
                    if n_localidad == "0":
                        print("Saliendo al menu de consulta del clima")
                        break
                    elegido_localidad = elegido.localidades[int(n_localidad)-1]
                    
                    print(f"Consultando el clima en tiempo real para {elegido_localidad.nombre}...") 
                    
                    # Rosilllll, que funcion usooo?
                    
            if opcion == "2": # Buscar por nombre de la localidad
                pass
                        
    def reportes_estadisticas(self):
        print("Menu reportes y estadisticas")
        pass

    def historicos(self):
        print("Menu historicos")
        pass