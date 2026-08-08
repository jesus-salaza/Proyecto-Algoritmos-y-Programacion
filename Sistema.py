from Municipio import Municipio
from Localidad import Localidad
from Clima import Clima
from Consulta import Consulta
from funciones import *
from api import *
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
        """ Metodo que carga los municipios del json y genera el reporte en pantalla indicando 
        por cada municipio:
            - Cantidad de localidades cargadas.
            - Cantidad de localidades con coordenadas geográficas.
            - Cantidad de localidades sin coordenadas geográficas conocidas.
            - Porcentaje de localidades con coordenadas geográficas.
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
        
        # Reporte
        print("\n ---------- REPORTE DE MUNICIPIOS Y LOCALIDADES ----------\n")
        for municipio in self.municipios:
            total_localidades = len(municipio.localidades)
            localidades_con_coordenadas = 0
            localidades_sin_coordenadas = 0
            for localidad in municipio.localidades:
                if localidad.latitud and localidad.longitud:
                    localidades_con_coordenadas += 1
                else:
                    localidades_sin_coordenadas += 1
            
            if total_localidades > 0:
                porcentaje_con_coordenadas = (localidades_con_coordenadas / total_localidades) * 100  
            else:
                porcentaje_con_coordenadas = 0
            
            print(f"Municipio: {municipio.nombre}")
            print(f"Cantidad de localidades cargadas: {total_localidades}")
            print(f"Cantidad de localidades con coordenadas geográficas: {localidades_con_coordenadas}")
            print(f"Cantidad de localidades sin coordenadas geográficas conocidas: {localidades_sin_coordenadas}")
            print(f"Porcentaje de localidades con coordenadas geográficas: {porcentaje_con_coordenadas:.2f}%\n")
        
            
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
                    
                    # Se solicita el municipio y la localidad
                    titulo = "Selección del municipio"
                    n_municipio = elegir_opcion(self.nombres_municipios, titulo, True)
                    if n_municipio == "0":
                        print("\nSaliendo al menu de consulta del clima...")
                        break
                    elegido = self.municipios[int(n_municipio)-1] # Nombre del municipio
                    
                    titulo = "Selección de la localidad"
                    localidades_disponibles = []
                    for localidad in elegido.localidades:
                        if localidad.latitud and localidad.longitud:
                            localidades_disponibles.append(localidad.nombre)  
                            
                    n_localidad = elegir_opcion(localidades_disponibles, titulo,True)
                    if n_localidad == "0":
                        print("\nSaliendo al menu de consulta del clima...")
                        break
                    
                    contador = 0
                    indice = 0
                    elegido_localidad = None
                    for localidad in elegido.localidades:
                        indice += 1
                        if localidad.latitud and localidad.longitud:
                            contador += 1
                        if contador == int(n_localidad):
                            elegido_localidad = localidad
                            break
                        
                    if not elegido_localidad.latitud or not elegido_localidad.longitud:
                        print(f"\nLa localidad {elegido_localidad.nombre} no tiene coordenadas geográficas registradas actualmente. No se puede consultar el clima en tiempo real, intente luego.\n")
                        continue
                    
                    print(f"\nConsultando el clima en tiempo real para {elegido_localidad.nombre}...\n") 
                    
                    # Se consulta el clima llamando a la API
                    datos_clima = consultar_clima_por_coordenadas(elegido_localidad.latitud, elegido_localidad.longitud)
                    
                    if datos_clima:
                        fecha_hora = datos_clima["fecha_hora"]
                        clima = Clima(
                            datos_clima["temperatura"],
                            datos_clima["humedad"],
                            datos_clima["viento"],
                            datos_clima["codigo_tiempo"],
                            datos_clima["estado_tiempo"]
                        )
                        elegido_localidad.cambiar_clima_actual(clima)
                        #elegido.mostrar_detalles(indice-1)
                    
                        # Se crea y guarda una consulta
                        nueva_consulta = Consulta(fecha= fecha_hora,municipio=elegido,posicion_localidad=indice-1)
                        nueva_consulta.mostrar_detalles() # Se muestra al usuario
                        self.consultas.append(nueva_consulta)
                    
            if opcion == "2": # Buscar por nombre de la localidad
                while True:
                    
                    # Se solicita el nombre al usuario
                    nombre_localidad = input(f"\nIngrese el nombre de la localidad (o '0' para salir): ")
                    if nombre_localidad == "0":
                        print("\nSaliendo al menu de consulta del clima...")
                        break
            
                    # Se consulta con el nombre buscando por coincidencia parcial y permitiendo seleccionar entre las coincidencias de su busqueda
                    datos_clima = consultar_clima_por_nombre_localidad(nombre_localidad, self.municipios)
                    if datos_clima is None:
                        print("\nSaliendo al menu de consulta del clima...")
                        break
                    if datos_clima:
                        municipio = datos_clima["municipio"]
                        posicion_localidad = datos_clima["posicion_localidad"]
                        fecha_hora = datos_clima["fecha_hora"]
                        clima = Clima(
                            datos_clima["temperatura"],
                            datos_clima["humedad"],
                            datos_clima["viento"],
                            datos_clima["codigo_tiempo"],
                            datos_clima["estado_tiempo"]
                        )
                        
                        # Se crea la consulta
                        nueva_consulta = Consulta(
                            fecha= fecha_hora,
                            municipio=municipio,
                            posicion_localidad=posicion_localidad
                        )
                        nueva_consulta.mostrar_detalles() # Se muestra al usuario
                        self.consultas.append(nueva_consulta)
                        break
                        
    def reportes_estadisticas(self):
        
        titulo = "Reportes y Estadísticas"
        
        # De las consultas de la sesion actual 
        temperaturas = []
        if self.consultas:
            for consulta in self.consultas:
                municipio = consulta.municipio
                posicion_localidad = consulta.posicion_localidad
                localidad = municipio.localidades[posicion_localidad]
                if localidad.clima:
                    temperaturas.append((municipio.nombre, localidad.nombre, localidad.clima.temperatura))

            # Municipio con la temperatura más cálida y mas fría 
            if temperaturas:
                municipio_mas_calido = '' 
                municipio_mas_frio = ''
                for municipio, localidad, temperatura in temperaturas:
                    if not municipio_mas_calido or temperatura > municipio_mas_calido[2]:
                        municipio_mas_calido = (municipio, localidad, temperatura)
                    if not municipio_mas_frio or temperatura < municipio_mas_frio[2]:
                        municipio_mas_frio = (municipio, localidad, temperatura)
                        
            # Cobertura
            localidades_sin_coordenadas = {}
            for municipio in self.municipios:
                localidades_sin_coordenadas[municipio.nombre] = []
                for localidad in municipio.localidades:
                    if not localidad.latitud or not localidad.longitud:
                        localidades_sin_coordenadas[municipio.nombre].append(localidad.nombre)
            
            # Promedio general
            suma_temperaturas = 0
            for tupla in temperaturas:
                temperatura = tupla[2]
                try:
                    valor_temperatura = float(temperatura.split()[0])  # Extraer el valor numérico de la temperatura
                    suma_temperaturas += valor_temperatura
                except ValueError:
                    print(f"Advertencia: No se pudo convertir la temperatura '{temperatura}' a número.")
            
            promedio_general = suma_temperaturas / len(temperaturas)
            
            print(f"\n ---------- {titulo} ----------\n")
            print(f"Cantidad de consultas realizadas en la sesión: {len(self.consultas)}")
            print("\n ----- Ranking de temperatura -----")
            print(f"Municipio con la localidad más cálida: {municipio_mas_calido[0]} - Localidad: {municipio_mas_calido[1]} - Temperatura: {municipio_mas_calido[2]}")
            print(f"Municipio con la localidad más fría: {municipio_mas_frio[0]} - Localidad: {municipio_mas_frio[1]} - Temperatura: {municipio_mas_frio[2]}")
            print("\n ----- Cobertura Geográfica -----")
            print("Localidades sin coordenadas registradas:")
            
            for municipio, localidades in localidades_sin_coordenadas.items():
                if localidades:
                    print(f"\n  Municipio: {municipio}")
                    cantidad_localidades_por_fila = 4  # Cantidad a imprimir por fila 
            
                    # i va de 3 en 3 (0, 3, 6, 9...)
                    for i in range(0, len(localidades), cantidad_localidades_por_fila):
                        # toma solo 3 localidades para la fila
                        grupo = localidades[i : i + cantidad_localidades_por_fila]

                        fila = ""
                        for localidad in grupo:
                            # .ljust(36) rellena con espacios al final hasta completar 35 caracteres
                            texto_alineado = f"- {localidad}".ljust(36)
                            fila = fila + texto_alineado  # Vamos pegando cada localidad

                        print("    " + fila)
            
            print("\n ----- Promedio general -----")        
            print(f"\nPromedio general de temperatura de las localidades consultadas: {promedio_general:.2f} °C")
            
        else:
            print("\nNo se han realizado consultas de clima en esta sesión.")

    def historicos(self):
        while True:
            titulo = "Históricos"
            print(f"\n ---------- {titulo} ----------")
            
            # Se solicita municipio y localidad
            titulo = "Selección del municipio"
            n_municipio = elegir_opcion(self.nombres_municipios, titulo, True)
            if n_municipio == "0":
                print("\nSaliendo al menu de consulta del clima...")
                break
            elegido = self.municipios[int(n_municipio)-1] # Nombre del municipio
            
            titulo = "Selección de la localidad"
            localidades_disponibles = []
            for localidad in elegido.localidades:
                if localidad.latitud and localidad.longitud:
                    localidades_disponibles.append(localidad.nombre)  
                    
            n_localidad = elegir_opcion(localidades_disponibles, titulo,True)
            if n_localidad == "0":
                print("\nSaliendo al menu de consulta del clima...")
                break
            
            contador = 0
            indice = 0
            elegido_localidad = None
            for localidad in elegido.localidades:
                indice += 1
                if localidad.latitud and localidad.longitud:
                    contador += 1
                if contador == int(n_localidad):
                    elegido_localidad = localidad
                    break

            if not elegido_localidad.latitud or not elegido_localidad.longitud:
                print(f"\nLa localidad {elegido_localidad.nombre} no tiene coordenadas geográficas registradas actualmente. No se puede consultar el clima en tiempo real, intente luego.\n")
                continue
            
            # Se solicita la fecha, el rango valido es de hasta 3 meses atras 
            hoy = datetime.now().date()
            try:
                hace_cinco_años = hoy.replace(year=hoy.year - 5)
            except ValueError:
                hace_cinco_años = hoy.replace(year=hoy.year - 5, day=28)
        
            print(f"\n--- Selección de Período para {elegido_localidad.nombre} ---")
            print(f"Rango permitido: desde {hace_cinco_años} hasta {hoy}")
            
            fecha_inicio = solicitar_fecha("\nIngrese la fecha de inicio (AAAA-MM-DD): ", hace_cinco_años, hoy)
            fecha_fin = solicitar_fecha("Ingrese la fecha de fin (AAAA-MM-DD): ", fecha_inicio, hoy)
            
            # Se consulta la api y se muestran los resultados
            print(f"\nConsultando el historico del clima para {elegido_localidad.nombre}...\n") 
            consultar_historicos_clima(elegido, elegido_localidad, fecha_inicio,fecha_fin)
                        