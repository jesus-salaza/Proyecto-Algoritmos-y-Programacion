"Archivo de funciones utiles para el sistema"

def validar_numero (numero, minimo=None, maximo=None):
    """ Funcion que valida si un numero es valido dentro de un rango dado

    Argumentos:
        numero (int): Numero a validar
        minimo (int): Valor minimo del rango
        maximo (int): Valor maximo del rango
    Retorna:
        bool: True si el numero es valido, False en caso contrario   
    """
    if numero < minimo or maximo < numero:
        return False
    return True

def elegir_opcion(lista_opciones, titulo="", personalizado=False):
    """ Funcion que permite al usuario elegir una opcion de una lista de 
    opciones dada

    Argumentos:
        lista_opciones (_list(str)): Lista de las opciones a elegir
        titulo (str): Titulo del menu
        personalizado (bool): Indica si se debe mostrar el menu de 
        forma personalizada

    Retorna:
        int: Opcion elegida por el usuario
        
    """
    if personalizado:
        print(f" ----- {titulo} ----- \n")
        for option in lista_opciones:
            print(f"    {lista_opciones.index(option)+1}. {option}")
        selected = input("Seleccione una opcion o ingrese 0 para salir: ")
        while not validar_numero(int(selected), 0, len(lista_opciones)):
            print("     Opcion invalida")
            selected = input("Seleccione una opcion o ingrese 0 para salir: ")
        return selected
        
    else:
        for option in lista_opciones:
            print(f"{lista_opciones.index(option)+1}. {option}")
        selected = input("Seleccione una opcion o ingrese 0 para salir: ")
        while not validar_numero(int(selected), 0, len(lista_opciones)):
            print("     Opcion invalida")
            selected = input("Seleccione una opcion o ingrese 0 para salir: ")
        return selected