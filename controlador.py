from tkinter import Tk
from vista import VentanaPP

class Controler():
#Inicializa la vista.
    
    def __init__(self, ventana):
        self.ventana = ventana
        self.obj_ventana = VentanaPP(ventana)

if __name__=="__main__":
    ventana = Tk()
    aplicacion = Controler(ventana)
    ventana.mainloop()