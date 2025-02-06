import socketserver
from modelo_ORM import BaseDatos
from log.log_actividad import LogReg

class MyTCPHandler(socketserver.BaseRequestHandler):
    '''
    Clase dedicada a la creacion de socketserver.
    '''
    def handle(self):
        '''
        Se instacia la clase BaseDatos para recuperar registros y se retorna al cliente.
        '''
        bd=BaseDatos()
        self.data = self.request.recv(1024).decode('ascii')
        try:    
            sectores= bd.recuperarSectoresDB(self.data)
            total_consumo_sec=0
            for sector in sectores:
                total_consumo_sec= total_consumo_sec + sector.fase
            # enviar al cliente
            self.request.sendall(str(total_consumo_sec).encode('ascii'))
            # log
            log = LogReg()
            log.log_server(self.client_address[0], self.data)
        except:
            self.request.sendall("Seleccione una opcion").encode('ascii')
        
if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        
        server.serve_forever()
        
