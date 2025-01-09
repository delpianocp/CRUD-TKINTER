from peewee import Model
from peewee import MySQLDatabase, SqliteDatabase
from peewee import CharField, FloatField
import sys 
from reg_errores import RegError
from funcion_deco import registro_log

class SelectDB():
#Selecciona la base de datos a utilizar - "mysql" o "sqlite"    
        
    base_datos_seleccion= "sqlite" 
    
    def __init__(self):
        pass
    
    def selectMydb(self):
    #Retorna la instruccion de la base de datos a utilizar definida en la variable de clase.            
        
        try:
            if self.base_datos_seleccion == "mysql":
                db = MySQLDatabase(host="localhost", user="root", passwd="", database="mediciones")
                message="Se conecto con mysql"
                
            elif self.base_datos_seleccion == "sqlite":
                db = SqliteDatabase("registroMed.db")
                message="Se conecto con sqlite"
            return db
        except UnboundLocalError:
            mess_reg="Error en la asignacion de base de datos"
            print(mess_reg)       
            message=f"Ingrese correctamente el nombre de la base de datos, se ingreso '{self.base_datos_seleccion}'\nIngrese 'mysql' o 'sqlite' en la linea 8 de modelo_ORM.py"
            reg = RegError()
            reg.registrar_error("UnboundLocalError", mess_reg)
        finally:
            print(message)
    
database=SelectDB()
db=database.selectMydb() 

class BaseModel(Model):
    class Meta:
        database = db

class Mediciones(BaseModel):
    sector = CharField()
    fase = FloatField()
    fecha = CharField()
    hora = CharField()

try:
    db.connect()
    db.create_tables([Mediciones])

except AttributeError:
    mess_reg="No se encontro base de datos"
    print("Se interrumpe la aplicacion")
    reg = RegError()
    reg.registrar_error("AttributeError", mess_reg)
    sys.exit(0)

class BaseDatos():    
#Se define operaciones sobre la base de datos seleccionada.    
    
    def __init__(self,):
        pass
    @registro_log    
    def cargaDB(self, sector, fase, fecha, hora):
    #Inserta parametros en el modelo Mediciones.    
        
        mediciones=Mediciones()
        mediciones.sector= sector
        mediciones.fase= fase
        mediciones.fecha = fecha
        mediciones.hora= hora
        mediciones.save()

    def recuperarDB(self):
    #Recupera toda la tabla desde el modelo Mediciones.
        
        datadb = Mediciones.select()
        return datadb

    def recuperarFechasDB(self, fecha):
    #Retorna lista de cada registro de la tabla que contenga fecha.
        
        coleccion= Mediciones.select()
        lista_fechas = [] 
        
        for f in coleccion:
            if str(f.fecha) == str(fecha):
                lista_fechas.append(f)
            
        return lista_fechas  

    def recuperarSectoresDB(self, sector):
    #Retorna lista de cada registro de la tabla que contenga sector.
    
        coleccion= Mediciones.select()
        lista_sectores = [] 
        for s in coleccion:
            if str(s.sector) == str(sector):
                lista_sectores.append(s)
            
        return lista_sectores  
    
    @registro_log 
    def eliminarDB(self, elem_id):
    #Elimina registro segun id.
    
        reg_elim= Mediciones.get(Mediciones.id == elem_id)
        reg_elim.delete_instance()

    @registro_log 
    def modificarDB(self, elem_id, nuevo_sector, nueva_medicion, nueva_fecha, nueva_hora):
    #Modifica con nuevos valores el registro con el id pasado como parametro.
    
        actualizar=Mediciones.update(sector=nuevo_sector, fase = nueva_medicion, fecha = nueva_fecha, hora=nueva_hora).where(Mediciones.id == elem_id)
        actualizar.execute()
        
   