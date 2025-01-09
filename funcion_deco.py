from log_actividad import LogReg

def registro_log(funcion):
    def envoltura(*args):
        r=LogReg()
        if funcion.__name__ == "cargaDB":
            r.registrar_log(f'Se cargo =>{args[1]}, {args[2]}, {args[3]}, {args[4]}')
        elif funcion.__name__ == "eliminarDB":
            r.registrar_log(f'Se elimino el Id = {args[1]}')
        elif funcion.__name__ == "modificarDB":
            r.registrar_log(f'Se modifico el Id: {args[1]} => {args[2]}, {args[3]}, {args[4]}')
        return funcion(*args)
       
    return envoltura