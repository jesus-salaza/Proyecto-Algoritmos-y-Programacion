import requests

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
    