from datetime import timedelta, datetime
import re

def validacion_fecha(fecha):

    """
    Retorna True si fecha es menor o igual que fecha de actual.
    
    :param fecha: fecha a comparar.
    
    :Return: :True: Si fecha>fecha_hoy. 

    
    """
    fecha_hoy = datetime.now()
    
#Agrupa en el patron, dia y mes respectivamente, para formatear fecha y poder compararla como entero.
    patron_dia = re.search(r'^(\d{2})/\d{2}/\d{2}$', fecha)   
    patron_mes = re.search(r'^\d{2}/(\d{2})/\d{2}$', fecha)
    dia_cargado = patron_dia.group(1)   #Retorna el grupo () de patron_dia
    mes_cargado = patron_mes.group(1)
    
    mes_dia_cargado = f'{mes_cargado}{dia_cargado}'  #Se formatea la fecha como un entero sin "/" y mes por delante.

    if int(mes_dia_cargado) > int(fecha_hoy.strftime('%m/%d').replace("/", "")):
        
        return False
    else:
        return True 
    
def validacion_re_fase(fase):
    """
    Retorna True si realiza match en el patron definido.
    
    :param fase: Se le aplica patron utlizando el modulo re.
    
    :Return: :True: Si realiza match.
    
    """    
    patron1 = re.compile(r'^(0\.[1-9]|[1-9]\d?(\.\d)?|1[0-9][0-9]?(\.\d)?|2[0-9][0-9]?(\.\d)?|300(\.0+)?)$', re.I)
    if patron1.search(str(fase)):
        return True
    else:
        return False 
    
def datos_grafico(dataBD):
    """
    Retorna una tupla con 2 listas ordenadas, se utilizan para datos de grafico.
    
    :param dataBD: objeto de base de datos.
    
    :Return: lista_potencias_graf, lista_fechas_graf.
    
    """  
    
    listadb = []
    lista_tras = []
    for d in dataBD:
        listadb = [d.id, d.sector, d.fase, d.fecha, d.hora]
        lista_tras.append(listadb)
    
    lista_fechas_graf, lista_potencias_graf = [], []
    pot = 0     
       
    #Se crea lista_fecha_ult_10 como patron, para comparar con las fechas en db.
    
    #Se formatean los elementos en lista_fecha_ult_10 para q coincidan con fechas recuperadas en bd.
    
    lista_fecha_ult_10 = []
    cont = 10
    fecha_hoy = datetime.now()
    while cont != 0:
        fecha_ini = fecha_hoy - timedelta(days = cont)
        lista_fecha_ult_10.append(fecha_ini.strftime('%d/%m/%y'))  
        cont -= 1  
    lista_fecha_ult_10.append(fecha_hoy.strftime('%d/%m/%y'))  
    lista_fechasDB_ordenada = sorted(lista_tras, key=lambda fecha_ord : fecha_ord [3])  #Ordena todos los registros por fecha
    
    #Se comparan la fecha del regitro con las ultimas 10, se obtiene potencia para la fecha coincidente.
    for l in lista_fecha_ult_10:    
        for p in lista_fechasDB_ordenada:
            if p[3] == l:
                pot = pot + (p[2] * 220)/1000 
        if pot != 0:
            lista_potencias_graf.append(pot) 
            lista_fechas_graf.append(l)       
        pot = 0 
    return lista_potencias_graf, lista_fechas_graf   
 