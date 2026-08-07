from Clima import Clima
import requests
from funciones import *
import pandas as pd
from funciones import elegir_opcion

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
    """ Consulta en tiempo real la API de Open-Meteo usando latitud y longitud."""
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
    """  Consulta en tiempo real la API de Open-Meteo usando el nombre de la localidad."""
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
    
    if latitud is None or longitud is None:
        print(f"\nCoordenadas no disponibles para {municipio_elegido.localidades[posicion_localidad_elegida].nombre}.")
        return None
    
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


def consultar_historicos_clima(municipio_elegido, localidad_elegida, fecha_inicio,fecha_fin):
    """ Consulta de historico por periodo de tiempo de la API de Open-Meteo 
    """
    
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast"
    params = {
        "latitude": localidad_elegida.latitud,
        "longitude": localidad_elegida.longitud,
        "start_date": fecha_inicio.strftime("%Y-%m-%d"),
        "end_date": fecha_fin.strftime("%Y-%m-%d"),
        "hourly": ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"],
        "timezone": "auto"
    }

    print("\nConsultando API de Open-Meteo...")
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con la API: {e}")
        return

    hourly_data = data.get("hourly", {})
    if not hourly_data or "time" not in hourly_data:
        print("No se encontraron registros para el rango especificado.")
        return

    # Procesamiento con pandas como lo hace la documentacion de la api
    df = pd.DataFrame({
        "fecha_hora": pd.to_datetime(hourly_data["time"]),
        "temperatura": hourly_data["temperature_2m"],
        "humedad": hourly_data["relative_humidity_2m"],
        "precipitacion": hourly_data["precipitation"],
        "viento": hourly_data["wind_speed_10m"]
    })
    df.set_index("fecha_hora", inplace=True)

    # Valores por mes 
    df_mensual = df.resample("ME").agg({
        "temperatura": "mean",
        "humedad": "mean",
        "precipitacion": "sum",  # Precipitación acumulada
        "viento": "mean"
    })
    
    print(f" Reporte historico: {municipio_elegido.nombre} - {localidad_elegida.nombre}")
    print(f" Período analizado: {fecha_inicio} al {fecha_fin}")

    print("\n ----- Resumen mensual -----")
    for fecha_mes, fila in df_mensual.iterrows():
        print(f"\n   Mes: {fecha_mes.strftime('%B %Y').capitalize()}")
        print(f"      i.   Temperatura Promedio    : {fila['temperatura']:.2f} °C")
        print(f"      ii.  Humedad Relativa Prom.  : {fila['humedad']:.2f} %")
        print(f"      iii. Precipitación Acumulada : {fila['precipitacion']:.2f} mm")
        print(f"      iv.  Velocidad del Viento    : {fila['viento']:.2f} km/h")

    # Promedios de cada magnitud
    print("----- Valores promedios ----- ")
    print(f"   • Temperatura Promedio General : {df['temperatura'].mean():.2f} °C")
    print(f"   • Humedad Relativa Promedio    : {df['humedad'].mean():.2f} %")
    print(f"   • Precipitación Total Acumulada: {df['precipitacion'].sum():.2f} mm")
    print(f"   • Velocidad del Viento Promedio: {df['viento'].mean():.2f} km/h")

    # Año más caluroso, fresco, lluvioso y húmedo
    df['año'] = df.index.year
    df_anual = df.groupby('año').agg({
        'temperatura': 'mean',
        'humedad': 'mean',
        'precipitacion': 'sum',
        'viento': 'mean'
    })

    print("----- Comparativa de año más caluroso, fresco, lluvioso y húmedo ----- ")

    año_caluroso = df_anual['temperatura'].idxmax()
    año_fresco = df_anual['temperatura'].idxmin()
    año_lluvioso = df_anual['precipitacion'].idxmax()
    año_humedo = df_anual['humedad'].idxmax()

    print(f"   - Año más caluroso          : {año_caluroso} ({df_anual.loc[año_caluroso, 'temperatura']:.2f} °C)")
    print(f"   - Año más fresco            : {año_fresco} ({df_anual.loc[año_fresco, 'temperatura']:.2f} °C)")
    print(f"   - Año con mayor precipitación: {año_lluvioso} ({df_anual.loc[año_lluvioso, 'precipitacion']:.2f} mm acumulados)")
    print(f"   - Año con mayor humedad     : {año_humedo} ({df_anual.loc[año_humedo, 'humedad']:.2f} %)")

    # Gráfico
    generar_graficos_historicos(df, localidad_elegida.nombre)