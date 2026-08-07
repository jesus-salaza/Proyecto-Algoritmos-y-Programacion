"Archivo de funciones utiles para el sistema"
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

def validar_numero (numero, minimo=None, maximo=None):
    """ Funcion que valida si un numero es valido dentro de un rango dado

    Argumentos:
        numero (int): Numero a validar
        minimo (int): Valor minimo del rango
        maximo (int): Valor maximo del rango
    Retorna:
        bool: True si el numero es valido, False en caso contrario   
    """
    try:
        numero = int(numero)
    except (ValueError, TypeError):
        return False

    if numero < minimo or maximo < numero:
        return False
    return True

def elegir_opcion(lista_opciones, titulo="", personalizado=False):
    """ Funcion que permite elegir una opcion de una lista de opciones dada

    Argumentos:
        lista_opciones (_list(str)): Lista de las opciones a elegir
        titulo (str): Titulo del menu
        personalizado (bool): Indica si se debe mostrar el titulo 

    Retorna:
        int: Opcion elegida por el usuario
        
    """
    if personalizado:
        print(f"\n ----- {titulo} ----- \n")
        for opcion in lista_opciones:
            print(f"    {lista_opciones.index(opcion)+1}. {opcion}")
        seleccionada = input("\nSeleccione una opcion o ingrese 0 para salir: ")
        while not validar_numero(seleccionada, 0, len(lista_opciones)):
            print("     Opcion invalida")
            seleccionada = input("\nSeleccione una opcion o ingrese 0 para salir: ")
        return seleccionada
        
    else:
        for opcion in lista_opciones:
            print(f"{lista_opciones.index(opcion)+1}. {opcion}")
        seleccionada = input("Seleccione una opcion o ingrese 0 para salir: ")
        while not validar_numero(seleccionada, 0, len(lista_opciones)):
            print("     Opcion invalida")
            seleccionada = input("Seleccione una opcion o ingrese 0 para salir: ")
        return seleccionada 
                 
def solicitar_fecha(mensaje, fecha_minima, fecha_maxima):
    """  Solicita una fecha al usuario en formato AAAA-MM-DD y la valida dentro de un rango."""
    while True:
        entrada = input(mensaje).strip()
        try:
            fecha = datetime.strptime(entrada, "%Y-%m-%d").date()
            if fecha < fecha_minima or fecha > fecha_maxima:
                print(f"La fecha debe estar entre {fecha_minima} y {fecha_maxima}.")
            else:
                return fecha
        except ValueError:
            print("Formato inválido. Debe usar AAAA-MM-DD (ejemplo: 2026-06-15).")


def generar_graficos_historicos(df, nombre_localidad):
    """ Muestra un gráfico de 4 subpaneles del historico para los tados meteorologicos

    Args:
        df (DataFrame de pandas): Objeto dataframe 
        nombre_localidad (str): nombre de la localidad para el titulo
    """    
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f"Historico de datos meteorológicos - {nombre_localidad}", fontsize=14, fontweight='bold')

    # 1. Temperatura
    axes[0, 0].plot(df.index, df['temperatura'], color='tab:red', linewidth=1)
    axes[0, 0].set_title("Temperatura (°C)")
    axes[0, 0].set_ylabel("°C")
    axes[0, 0].grid(True, linestyle='--', alpha=0.6)

    # 2. Humedad
    axes[0, 1].plot(df.index, df['humedad'], color='tab:blue', linewidth=1)
    axes[0, 1].set_title("Humedad relativa (%)")
    axes[0, 1].set_ylabel("%")
    axes[0, 1].grid(True, linestyle='--', alpha=0.6)

    # 3. Precipitación
    axes[1, 0].plot(df.index, df['precipitacion'], color='tab:cyan', linewidth=1)
    axes[1, 0].set_title("Precipitación (mm)")
    axes[1, 0].set_ylabel("mm")
    axes[1, 0].grid(True, linestyle='--', alpha=0.6)

    # 4. Viento
    axes[1, 1].plot(df.index, df['viento'], color='tab:green', linewidth=1)
    axes[1, 1].set_title("Velocidad del viento (km/h)")
    axes[1, 1].set_ylabel("km/h")
    axes[1, 1].grid(True, linestyle='--', alpha=0.6)

    plt.tight_layout()
    print("\nAbriendo gráfico en pantalla...")
    plt.show()


