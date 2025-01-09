import os
import datetime

class LogReg():

    BASE_DIR = os.path.dirname((os.path.abspath(__file__)))
    ruta = os.path.join(BASE_DIR, "log-reg.txt")

    def __init__(self):
        pass


    def registrar_log(self, *args):
        
        log = open(self.ruta, "a")
        print(f"{args}  Fecha: {datetime.datetime.now()}\n\n" , file=log)
