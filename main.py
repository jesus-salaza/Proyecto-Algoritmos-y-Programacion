from Sistema import Sistema

def main():
    """ Función que crea un objeto de la clase Sistema e inicia el programa
    El programa necesita tener instalada OpenMeteo-request 
    """    
    sistema = Sistema()
    sistema.iniciar()    
    
main()
