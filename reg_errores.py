import os
import datetime

class RegError(Exception):
#Guarda registro de errores.
    
    BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
    ruta = os.path.join(BASE_DIR, "reg_errores.txt")

    def __init__(self):
        pass

    def registrar_error(self, error, mensaje):
    #Registra en un archivo el error y mensaje recibidos.    
        
        log = open(self.ruta, "a")
        print(f"{mensaje} \nTipo de error: {error}  Fecha: {datetime.datetime.now().strftime('%d/%m/%y')} Hora: {datetime.datetime.now().strftime('%H:%M')} \n\n" , file=log) #datetime.now().strftime('%d/%m/%y')

