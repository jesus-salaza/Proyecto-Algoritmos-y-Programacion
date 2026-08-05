from Clima import Clima
import requests
from funciones import *

" Codigos de la API de OpenMeteo del parametro weather_code, segun la documentacion oficial. "
traductor_weather_codes = {
    0: "Despejado",
    1: "Mayormente despejado",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Niebla",
    48: "Niebla con escarcha",
    51: "Llovizna ligera",
    53: "Llovizna moderada",
    55: "Llovizna densa",
    61: "Lluvia ligera",
    63: "Lluvia moderada",
    65: "Lluvia fuerte",
    71: "Nevada ligera",
    73: "Nevada moderada",
    75: "Nevada fuerte",
    80: "Chubascos ligeros",
    81: "Chubascos moderados",
    82: "Chubascos violentos",
    95: "Tormenta eléctrica",
    96: "Tormenta eléctrica con granizo ligero",
    99: "Tormenta eléctrica con granizo fuerte"
}

def consultar_clima_por_coordenadas(latitud, longitud):
    """
    Consulta en tiempo real la API de Open-Meteo usando latitud y longitud.
    Despliega en pantalla todos los datos del clima requeridos.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "weather_code"],
        "timezone": "auto"
    }

    try:
        response = requests.get(url, params=parametros)
        response.raise_for_status()
        data = response.json()
        #print(data)  

        fecha_hora = data.get("current", {}).get("time", "N/A")
        actual = data.get("current", {})
        unidades = data.get("current_units", {})

        # Obtener interpretación del código meteorológico
        codigo = actual.get("weather_code", 0)
        estado_traducido = traductor_weather_codes.get(codigo, f"Desconocido (Código {codigo})")

        # Podemos cambiar esto dependiendo como lo queramos
        resultado = {
            "fecha_hora": fecha_hora,
            "latitud": latitud,
            "longitud": longitud,
            "temperatura": f"{actual.get('temperature_2m')} {unidades.get('temperature_2m', '°C')}",
            "humedad": f"{actual.get('relative_humidity_2m')} {unidades.get('relative_humidity_2m', '%')}",
            "viento": f"{actual.get('wind_speed_10m')} {unidades.get('wind_speed_10m', 'km/h')}",
            "codigo_tiempo": codigo,
            "estado_tiempo": estado_traducido
        }
        
        return resultado

    except requests.exceptions.RequestException as e:
        print(f"Error de conexion con la API de Open-Meteo: {e}")
        return {}
    
def consultar_clima_por_nombre_localidad(nombre_localidad, municipios):
    """
    Consulta en tiempo real la API de Open-Meteo usando el nombre de la localidad.
    Despliega en pantalla todos los datos del clima requeridos.
    """
    # Busco si alguna localidad coincide parcialmente con el nombre ingresado
    coincidencias = []
    for municipio in municipios:
        for localidad in municipio.localidades:
            if nombre_localidad.lower() in localidad.nombre.lower():
                posicion_localidad = municipio.localidades.index(localidad)
                coincidencias.append((municipio, posicion_localidad))

    if not coincidencias:
        print(f"\nNo se encontraron localidades que coincidan con '{nombre_localidad}'. Intente nuevamente.\n")
        return

    titulo = "Selección de la localidad"
    opciones_localidades = []
    for municipio, posicion_localidad in coincidencias:
        opciones_localidades.append(f"{municipio.nombre} - {municipio.localidades[posicion_localidad].nombre}")

    n_localidad = elegir_opcion(opciones_localidades, titulo, True)
    if n_localidad == "0":
        print("\nSaliendo al menu de consulta del clima...")
        return None
    
    municipio_elegido, posicion_localidad_elegida = coincidencias[int(n_localidad)-1]
    
    latitud = municipio_elegido.localidades[posicion_localidad_elegida].latitud
    longitud = municipio_elegido.localidades[posicion_localidad_elegida].longitud                    
    resultado = consultar_clima_por_coordenadas(latitud, longitud)
    nuevo_clima = Clima(
    resultado["temperatura"],
    resultado["humedad"],
    resultado["viento"],
    resultado["codigo_tiempo"],
    resultado["estado_tiempo"]
    )
    
    municipio_elegido.localidades[posicion_localidad_elegida].cambiar_clima_actual(nuevo_clima)
    resultado["municipio"] = municipio_elegido
    resultado["posicion_localidad"] = posicion_localidad_elegida
    
    return resultado
