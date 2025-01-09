import tkinter
from tkinter import ttk, PhotoImage
from tkinter import StringVar
from tkinter import Frame
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from validaciones import validacion_fecha
from validaciones import validacion_re_fase
from validaciones import datos_grafico
from modelo_ORM import BaseDatos
from tktimepicker import AnalogPicker, AnalogThemes, constants
import os
from PIL import ImageTk,Image

class VentanaPP():
    
    def __init__(self, ventana):
        self.ventana_principal=ventana    
        self.ventana_principal.geometry("950x600")
        self.ventana_principal.title("Bienvenido a registros de potencias")
        self.ventana_principal.resizable(width=False, height=False)   
        self.ventana_principal.configure(background='SlateBlue4')
        self.obj_db = BaseDatos()
        
        dir_img = f'{os.path.dirname(__file__)}/image'
        self.logo_img = ImageTk.PhotoImage(Image.open(os.path.join(dir_img, "logo.png")))
        self.logo = Label(image = self.logo_img, bg="SlateBlue4")
        self.logo.place(x=20, y = 550)
        
        ################# VARIABLES INGRESADAS POR USUARIO ##################################
        
        self.fase, self.fecha, self.hora, self.minuto, self.sector, self.sel_bd, self.sel_base = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.nueva_fase, self.nueva_fecha, self.nueva_hora, self.nuevo_minuto, self.nuevo_sector = StringVar(), StringVar(), StringVar(), StringVar(), StringVar()
        self.sector_buscar, self.fecha_buscar = StringVar(), StringVar()
        
        #####################################################################################
        l_hora, l_min = [], []
        l_sectores = ["Sistemas", "Servidor", "Seguridad", "Sala de maquinas", "Taller"]
        for l in range(0, 24):
            l_hora.append(f"{l:02d}")
        for i in range(0, 60):
            l_min.append(f"{i:02d}") 
        
        #############FRAME CARGA###################
        self.frame_carga = Frame(self.ventana_principal, width = 250, height = 250, bg='SlateBlue1')
        self.titulo_frame_carga = Label(self.frame_carga, text="Carga", font=("Arial",12), width = 25, bg='turquoise1')
        self.frame_carga.config(relief="sunken")   
        self.frame_carga.config(bd=1)  

        self.sector_label = Label(self.frame_carga, text="Sector", bg='SlateBlue1')
        self.s = ttk.Combobox(
            self.frame_carga,
            state="readonly",
            values=l_sectores,
            font=("Arial",12),
            width=10,
            textvariable=self.sector
            )
        self.sector.set("")

        self.fase_label = Label(self.frame_carga, text="Fase  (Amp)", bg='SlateBlue1')
        self.f = Entry(self.frame_carga, textvariable=self.fase, width=8, font=("Arial",12))
        self.fase.set("")
        
        self.tiempo_label = Label(self.frame_carga, text="Hora", bg='SlateBlue1')
        self.time_label = Label(self.frame_carga, text="--:--", bg='SlateBlue1', font=("Arial",12))
        self.time_boton = Button(self.frame_carga, text="Ingresar hora", command=lambda: self.get_tiempo(),font=("Arial", 8), bg="turquoise1")
        self.minuto = "--"
        self.hora = "--"
        
       
        self.fecha_label = Label(self.frame_carga, text="Fecha", bg='SlateBlue1')
        self.fe = DateEntry(self.frame_carga, width=10, textvariable = self.fecha, date_pattern="dd/mm/yy", background='darkblue', foreground='white', font=("Arial",12), borderwidth=2, selectmode = 'day')

        self.boton_enviar=Button(self.frame_carga, text="Cargar Medicion", command=lambda: self.cargar() ,font=("Arial", 8), bg="turquoise1")
        self.boton_modificar=Button(self.frame_carga, text="Modificar",command=lambda: self.set_var_modificacion(), font=("Arial", 8), bg="orange")
        self.boton_eliminar=Button(self.frame_carga, text="Eliminar",command=lambda: self.eliminar(), font=("Arial", 8), bg="red")
                
        self.frame_carga.grid(padx = 5, pady = 5,column= 0, row= 0, sticky='nsew')
        self.titulo_frame_carga.grid(column=0, columnspan=2, row=0, sticky='w')
        self.sector_label.grid(padx = 5, pady = 5,column= 0, row= 1, sticky='w')
        self.s.grid(padx = 5, pady = 5,column= 1, row= 1, sticky='w')
        self.fase_label.grid(padx = 5, pady = 5, column= 0, row= 5, sticky='w')
        self.f.grid(padx = 5, pady = 5, column= 1, row= 5, sticky='w')
        self.time_label.grid(padx = 5, pady = 5, column= 1, row= 3, sticky='w')
        self.time_boton.grid(padx = 5, pady = 5, column= 1, row= 4, sticky='w')
        self.tiempo_label.grid(padx = 5, pady = 5, column= 0, row= 3, sticky='w')
        self.fecha_label.grid(padx = 5, pady = 5, row = 2, column= 0, sticky='w')
        self.fe.grid(padx = 5, pady = 5, row = 2, column= 1, sticky='w')
        self.boton_enviar.grid(padx = 5, pady = 15, column= 0,columnspan=2, row= 6, sticky='nsew')
        self.boton_eliminar.grid(padx = 5, column= 0, row= 7, sticky='ew')
        self.boton_modificar.grid(padx = 5, pady = 5, column= 1, row= 7, sticky='nsew')

        #################FRAME TREEVIEW####################################
        self.frame_bd = Frame(self.ventana_principal, width = 550, height = 270, bg='SlateBlue4')
        self.frame_bd.config(relief="sunken")   
        self.frame_bd.config(bd=5)             

        self.tabla = ttk.Treeview(self.frame_bd, height = 12)
        self.tabla["columns"] = ('sector', 'ampere', 'dia', 'hora')
        self.tabla.column("#0", width=40, minwidth=20)
        self.tabla.column("sector", width=100)
        self.tabla.column("ampere", width=100)
        self.tabla.column("dia", width=100)
        self.tabla.column("hora", width=100)
        self.tabla.heading('#0', text = 'Id')
        self.tabla.heading('sector', text = 'Sector')
        self.tabla.heading('ampere', text = 'Ampere')
        self.tabla.heading('dia', text = 'Fecha')
        self.tabla.heading('hora', text = 'Hora')
        self.tabla.bind("<Double-Button-1>", self.set_var_modificacion_event)
        self.frame_bd.grid(padx = 5, pady = 10, column= 1, row= 0, sticky='nsew')
        self.tabla.grid(column=0, row=0, sticky='nsew')

        #######################FRAME BUSQUEDA############################
        self.frame_busqueda = Frame(self.ventana_principal, width = 250, height = 250, bg='SlateBlue1')
        self.titulo_frame_busqueda = Label(self.frame_busqueda, text="Buscar", font=("Arial",12), width = 25, bg='seaGreen1')
        self.frame_busqueda.config(relief="sunken")   
        self.frame_busqueda.config(bd=2)
        self.fecha_busqueda = Label(self.frame_busqueda, text="Fecha", bg='SlateBlue1')
        self.fecha_bus = DateEntry(self.frame_busqueda, width=12, textvariable= self.fecha_buscar, date_pattern="dd/mm/yy", background='darkblue',font=("Arial",12), foreground='white', borderwidth=2, selectmode = 'day')

        self.sector_busqueda = Label(self.frame_busqueda, text="Sector", bg='SlateBlue1', font=("Arial",8))
        self.s_bus = ttk.Combobox(
            self.frame_busqueda,
            state="readonly",
            values=l_sectores,
            font=("Arial",12),
            width=12,
            textvariable= self.sector_buscar
            )

        self.boton_buscar_fecha=Button(self.frame_busqueda, text="Buscar",font=("Arial", 8), command=lambda: self.busqueda_fecha(),  bg="seaGreen1")
        self.boton_buscar_sector=Button(self.frame_busqueda, text="Buscar",font=("Arial", 8), command=lambda: self.busqueda_sector(),  bg="seaGreen1")
        self.boton_mostrartodo=Button(self.frame_busqueda, text="Mostrar todo", command=lambda: self.cargar_treeview(), font=("Arial", 12), bg="seaGreen1")        
        self.frame_busqueda.grid(padx = 5, pady = 5,column= 0, row= 1, sticky='nsew')
        self.titulo_frame_busqueda.grid(column=0, columnspan=2, row=0, sticky='w')
        self.fecha_busqueda.grid(padx = 5, pady = 5, row = 1, column= 0)
        self.fecha_bus.grid(padx = 5, pady = 5, row = 1, column= 1)
        self.boton_buscar_fecha.grid(padx = 5, pady = 5, row = 2, column= 1)
        self.sector_busqueda.grid(padx = 5, pady = 5, row = 4, column= 0)
        self.s_bus.grid(padx = 5, pady = 5, row = 4, column= 1)
        self.boton_buscar_sector.grid(padx = 5, pady = 5, row = 5 , column= 1)
        self.boton_mostrartodo.grid(padx = 5, pady = 20, row = 6, column= 0, columnspan= 2, sticky='nsew')

        ###############FRAME MODIFICAR######################
        self.frame_modificar = Frame(self.ventana_principal, width = 250, height = 250, bg='SlateBlue1')
        self.titulo_frame_modificar = Label(self.frame_modificar, text="Modificar", font=("Arial",12), width = 25, bg='orange')
        self.frame_modificar.config(relief="sunken")   
        self.frame_modificar.config(bd=2) 
        self.nuevo_sector_label = Label(self.frame_modificar, text="Sector", bg='SlateBlue1')
        self.ns = ttk.Combobox(
            self.frame_modificar,
            state="readonly",
            values=l_sectores,
            font=("Arial",12),
            width=10,
            textvariable=self.nuevo_sector
            )
        self.nuevo_sector.set("")
        self.nueva_medicion_label = Label(self.frame_modificar, text="Fase  (Amp)", bg='SlateBlue1')
        self.nf = Entry(self.frame_modificar, textvariable =self.nueva_fase, width=8, font=("Arial",12))
        self.nueva_fase.set("")
        self.nueva_hora_label = Label(self.frame_modificar, text="Hora", font=("Arial",10), bg='SlateBlue1')
        self.nh = ttk.Combobox(
        self.frame_modificar,
        state="readonly",
        values=l_hora,
        font=("Arial",12),
        width="5",
        textvariable=self.nueva_hora
        )
        self.nueva_hora.set("--")
        self.nuevo_minutos_label = Label(self.frame_modificar, text="Minutos", font=("Arial",10), bg='SlateBlue1')
        self.nm = ttk.Combobox(
        self.frame_modificar,
        state="readonly",
        values=l_min,
        font=("Arial",12),
        width= "5",
        textvariable=self.nuevo_minuto
        )
        self.nuevo_minuto.set("--")
        self.nueva_fecha_label = Label(self.frame_modificar, text="Fecha", bg='SlateBlue1')
        self.nueva_f = DateEntry(self.frame_modificar, width=10, font=("Arial",12), textvariable=self.nueva_fecha, date_pattern="dd/mm/yy", background='darkblue', foreground='white', borderwidth=2, selectmode = 'day')

        self.boton_enviar_modificacion=Button(self.frame_modificar, text="Guardar Modificacion", command=lambda: self.modificar() ,font=("Arial", 8), bg="turquoise1", state=tkinter.DISABLED) # , state=self.ventana=DISABLED

        self.frame_modificar.grid(padx = 4, pady = 5,column= 2, row= 0, sticky='nsew')
        self.titulo_frame_modificar.grid(column=0, columnspan=2, row=0, sticky='w')
        self.nuevo_sector_label.grid(padx = 5, pady = 5,column= 0, row= 1, sticky='w')
        self.ns.grid(padx = 5, pady = 5,column= 1, row= 1, sticky='w')
        self.nueva_medicion_label.grid(padx = 5, pady = 15, row = 2, column= 0, sticky='w')
        self.nf.grid(padx = 5, pady = 15, row = 2, column= 1, sticky='w')
        self.nueva_hora_label.grid(padx = 5, pady = 5, column= 0, row= 3, sticky='w')
        self.nh.grid(padx = 5, pady = 5, column= 1, row= 3, sticky='w')
        self.nuevo_minutos_label.grid(padx = 5, pady = 5, column= 0, row= 4, sticky='w')
        self.nm.grid(padx = 5, pady = 5, column= 1, row= 4, sticky='w')
        self.nueva_fecha_label.grid(padx = 5, pady = 5, column= 0, row= 5, sticky='w')
        self.nueva_f.grid(padx = 5, pady = 5, column= 1, row= 5, sticky='w')
        self.boton_enviar_modificacion.grid(padx = 5, pady = 18, column= 0, columnspan=2, row= 6, sticky='nsew')

        self.boton_cerrar=Button(self.ventana_principal, text="Cerrar", command= lambda : self.cerrar() ,font=("Arial", 8))
        self.boton_cerrar.grid(padx = 5, pady = 5,column= 2, row= 2, sticky='nsew')
        
    def cargar(self):
        #valida variables, invoca a cargaDB() con las variables como argumento.
            
        if self.sector.get() == "":
            self.sector_label['bg'] = 'red'
            auth_sector=False
        else:
            self.sector_label['bg'] = 'SlateBlue1' 
            auth_sector=True
            
        if self.hora == "--":
            self.tiempo_label['bg'] = 'red'
            auth_hora=False
        else:
            self.tiempo_label['bg'] = 'SlateBlue1'
            auth_hora=True
            
        if self.minuto == "--":
            self.tiempo_label['bg'] = 'red'
            auth_minuto=False
        else:
            self.tiempo_label['bg'] = 'SlateBlue1'
            auth_minuto=True
                        
        if auth_hora and auth_minuto and auth_sector:
            
            if validacion_fecha(self.fecha.get()):
                self.fecha_label['bg'] = "SlateBlue1"
                auth_fecha=True
            else:    
                self.fecha_label['bg'] = "red"
                auth_fecha=False
                messagebox.showinfo(message=f"La fecha no puede ser superior a la de hoy {datetime.now().strftime('%d/%m/%y')}", title="Aviso")
            
            if validacion_re_fase(self.fase.get()):
                self.fase_label['bg'] = 'SlateBlue1' 
                auth_fase =True
            else:
                self.fase_label['bg'] = 'red' 
                auth_fase =False
                messagebox.showinfo(message="Admite valore entre 0.1 y 300", title="Aviso")
                            
            if auth_fecha and auth_fase:
                self.obj_db.cargaDB(self.sector.get(), float(self.fase.get()), self.fecha.get(), f"{self.hora}:{self.minuto}")
                self.cargar_treeview() 
                self.reset_var_carga()
                self.reset_var_modificacion()
                messagebox.showinfo(message="Medicion Agregada con exito", title="Aviso")
        else:
            messagebox.showinfo(message="Campos no completados", title="Aviso")
    
    def eliminar(self):
    #Si se selecciono un elemento de treeview, se recupera el id, y se invoca a eliminarDB con el id como argumento.
        
        if self.tabla.focus():    
        
            if messagebox.askokcancel(message="¿Desea Eliminar el elemento seleccionado?", title="Confirmacion"):
                elem = self.tabla.focus()
                elem_id = self.tabla.item(elem)['text']
                self.obj_db.eliminarDB(elem_id)
                self.cargar_treeview()
                self.reset_var_modificacion()
                messagebox.showinfo(message="El elemento fue eliminado", title="Aviso")
        else:
            messagebox.showinfo(message="Seleccione un elemento de la tabla", title="Aviso")  

    def cargar_treeview(self):
        self.reset_var_modificacion()
        self.limpiar_treeview()
        self.cargar_grafico()
        listabd= self.obj_db.recuperarDB()
        for l in listabd:
                self.tabla.insert(
        "", "end", text=l.id, values=(l.sector, l.fase, l.fecha, l.hora)
        ) 
    
    def limpiar_treeview(self):
    #Recupera todos los elemetos de treeview y elimina.
        for t in self.tabla.get_children():
            self.tabla.delete(t)
    
    def reset_var_carga(self):
    #Setea variables a valores iniciales del frame carga.   
        self.sector.set("")
        self.hora="--"
        self.minuto="--"
        self.fase.set("") 
        self.time_label['text'] = "--:--"
        
    
    def busqueda_fecha(self):
    #Recupera todos los registros coincidentes con fecha_buscar.    
        filas = self.obj_db.recuperarFechasDB(self.fecha_buscar.get())
        if filas:
            self.limpiar_treeview()
            for fila in filas:
                self.tabla.insert(
                "", "end", text=fila.id, values=(fila.sector, fila.fase, fila.fecha, fila.hora)
                )
            self.reset_var_modificacion()
        else:
            messagebox.showinfo(message="No se encontraron coincidencias", title="Aviso")
            
        
    def busqueda_sector(self):
    #Recupera todos los registros coincidentes con sector_buscar.
        lista_bus_sec = self.obj_db.recuperarSectoresDB(self.sector_buscar.get())
        if lista_bus_sec:
            self.limpiar_treeview()
            for fila in lista_bus_sec:      
                self.tabla.insert(
                "", "end", text=fila.id, values=(fila.sector, fila.fase, fila.fecha, fila.hora)
                )
            self.reset_var_modificacion()
        else:
            messagebox.showinfo(message="No se encontraron coincidencias", title="Funcion no disponible")
            
    def set_var_modificacion(self):
    #Obtiene el elemento de treeview y setea los campos del frame modificar con el elemento correspondiente.  
        global elem_id  #Se declara global para que pueda ser utilizado por modificar().
        if self.tabla.focus():
            elem = self.tabla.focus()
            elem_id = self.tabla.item(elem)['text']
            sector_treeview = self.tabla.item(elem)['values'][0]
            fase_treeview = self.tabla.item(elem)['values'][1]
            fecha_treeview = self.tabla.item(elem)['values'][2]
            hora_treeview = self.tabla.item(elem)['values'][3]
            self.limpiar_treeview()
            self.set_treview_modificacion(elem_id, sector_treeview, fase_treeview, fecha_treeview, hora_treeview)
            lista_hora = hora_treeview.split(":")  #Elimina ":" y retorna lista [hora, min]     
            self.nueva_hora.set(lista_hora[0])
            self.nuevo_minuto.set(lista_hora[1])
            self.boton_enviar_modificacion.config(state=tkinter.NORMAL)
            self.frame_modificar.config(bg="orange")
            self.nueva_medicion_label['bg'] = 'orange' 
            self.nueva_hora_label['bg'] = 'orange'
            self.nueva_fecha_label['bg'] = 'orange'
            self.nuevo_minutos_label['bg'] = 'orange'
            self.nuevo_sector_label['bg'] = 'orange'
            self.nueva_fase.set(fase_treeview) 
            self.nueva_f.set_date(fecha_treeview)
            self.nuevo_sector.set(sector_treeview)
        else:
            messagebox.showinfo(message="Seleccione un elemento de la tabla", title="Aviso")  
                               
    def modificar(self):
    #valida nuevas entradas, invoca a modificarDB con las nuevas variables como argumento. 
        
        if validacion_re_fase(self.nueva_fase.get()): 
            self.nueva_medicion_label['bg'] = 'orange'
            val_mod_fase = True 
        else:
            self.nueva_medicion_label['bg'] = 'red'     
            val_mod_fase = False 
            
        if validacion_fecha(self.nueva_fecha.get()):   
            self.nueva_fecha_label['bg'] = 'orange' 
            val_mod_fecha = True
        else:
            self.nueva_fecha_label['bg'] = 'red' 
            val_mod_fecha = False
        
        if val_mod_fase and val_mod_fecha:
            if messagebox.askokcancel(message="¿Desea Modificar el elemento seleccionado?", title="Confirmacion"):
                self.obj_db.modificarDB(elem_id, self.nuevo_sector.get(), float(self.nueva_fase.get()), self.nueva_fecha.get(), f"{self.nueva_hora.get()}:{self.nuevo_minuto.get()}")
                self.cargar_treeview()
                self.reset_var_modificacion()
                messagebox.showinfo(message="El elemento fue modificado", title="Aviso")

    def reset_var_modificacion(self):
    #Setea variables a valores iniciales del frame modificar.    
        self.nuevo_sector.set("")
        self.nueva_hora.set("--")
        self.nuevo_minuto.set("--")
        self.nueva_fase.set("")
        self.boton_enviar_modificacion.config(state=tkinter.DISABLED)
        self.frame_modificar.config(bg="SlateBlue1")
        self.nueva_medicion_label['bg'] = 'SlateBlue1' 
        self.nueva_hora_label['bg'] = 'SlateBlue1'
        self.nueva_fecha_label['bg'] = 'SlateBlue1'
        self.nuevo_minutos_label['bg'] = 'SlateBlue1'
        self.nuevo_sector_label['bg'] = 'SlateBlue1'
    
    def set_treview_modificacion(self, elem_id,sector_t, fase_t, fecha_t, hora_t):
    #limpia treeview y carga los valores del registro a modificar.
        
        self.tabla.insert("", "end", text=elem_id, values=(sector_t, fase_t, fecha_t, hora_t)) 

    def cargar_grafico(self):
    #Crea el area de grafico y sus propiedades.       
        datadb= self.obj_db.recuperarDB()
        self.frame_grafico = Frame(self.ventana_principal, width = 250, height = 250, bg='SlateBlue3')
        self.frame_grafico.config(relief="sunken")   
        self.frame_grafico.config(bd=1)
        fig, axs = plt.subplots(dpi=80, figsize=(8.67, 3))
        fig.suptitle('Consumo total de KW por dia (ultimos 10 Dias)')
        axs.bar(datos_grafico(datadb)[1], datos_grafico(datadb)[0], color = 'c')
        axs.set_ylabel('Potencia Kw')
        self.canvas = FigureCanvasTkAgg(fig, master = self.frame_grafico)  # Crea el area de dibujo en Tkinter.
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(column=0, row=0)
        self.frame_grafico.grid(padx = 5, pady = 5,column= 1, columnspan=2, row= 1, sticky='nsew')

    def cerrar(self):
    #Cierra la aplicacion.    
        if messagebox.askokcancel(message="¿Desea Salir de la aplicacion?", title="Confirmacion"):
            self.ventana_principal.quit()
            self.ventana_principal.destroy()
     
    def set_var_modificacion_event(self, event):
    #Obtiene el elemento de treeview y setea los campos del frame modificar con el elemento correspondiente.  
        global elem_id  #Se declara global para que pueda ser utilizado por modificar().
        
        elem = self.tabla.focus()
        elem_id = self.tabla.item(elem)['text']
        sector_treeview = self.tabla.item(elem)['values'][0]
        fase_treeview = self.tabla.item(elem)['values'][1]
        fecha_treeview = self.tabla.item(elem)['values'][2]
        hora_treeview = self.tabla.item(elem)['values'][3]
        self.limpiar_treeview()
        self.set_treview_modificacion(elem_id, sector_treeview, fase_treeview, fecha_treeview, hora_treeview)
        
        lista_hora = hora_treeview.split(":")  #Elimina ":" y retorna lista [hora, min].     
        self.nueva_hora.set(lista_hora[0])
        self.nuevo_minuto.set(lista_hora[1])
        self.boton_enviar_modificacion.config(state=tkinter.NORMAL)
        self.frame_modificar.config(bg="orange")
        self.nueva_medicion_label['bg'] = 'orange' 
        self.nueva_hora_label['bg'] = 'orange'
        self.nueva_fecha_label['bg'] = 'orange'
        self.nuevo_minutos_label['bg'] = 'orange'
        self.nuevo_sector_label['bg'] = 'orange'
        self.nueva_fase.set(fase_treeview) 
        self.nueva_f.set_date(fecha_treeview)
        self.nuevo_sector.set(sector_treeview)    

    def set_tiempo(self, time):
    #Asigna la hora a las variables de instancia self.hora y self.minuto.    
        
        self.time_label.configure(text="{}:{}".format(*time)) 
        self.hora = time[0]
        self.minuto = time[1]
        self.top.destroy()

    def get_tiempo(self):
    #Genera un Toplevel con el widget reloj.

        self.top = tkinter.Toplevel(self.ventana_principal)
        self.time_picker = AnalogPicker(self.top, type=constants.HOURS24)
        self.time_picker.pack(expand=True, fill="both")
        self.theme = AnalogThemes(self.time_picker)
        self.theme.setNavyBlue()
        self.ok_btn = Button(self.top, text="setear", command=lambda: self.set_tiempo(self.time_picker.time()))
        self.ok_btn.pack()
