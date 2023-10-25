import ttkbootstrap as ttk
from ttkbootstrap.toast import ToastNotification
from ttkbootstrap.constants import *
from ttkbootstrap.validation import add_regex_validation
from ttkbootstrap.tableview import Tableview
import tkinter as tk
from ttkbootstrap import Style, Frame, Button
import openpyxl
import sqlite3
from tkinter import simpledialog
class App(ttk.Frame):
    def __init__(self,ventana):
        ventana.withdraw()
        self.login()

        self.conn = sqlite3.connect("informe_pacientes.db")
        self.c = self.conn.cursor()
        self.crear_tabla_si_no_existe()

        # Interfaz principal
        self.ventana = ventana 
        self.colors = ventana.style.colors
        super().__init__(self.ventana, padding=(20, 10))
        self.pack(fill=ttk.BOTH, expand=tk.YES)

        self.nombre_paciente = ttk.StringVar(value="")
        self.numero_telefono = ttk.IntVar(value=0)
        self.motivo_cita = ttk.StringVar(value="")
        self.nivel_urgencia = ttk.DoubleVar(value=0)

        self.creacion_formulario("Nombre del paciente: ", self.nombre_paciente)
        self.creacion_formulario("Numero de telefono: ", self.numero_telefono)
        self.creacion_formulario("Motivo_cita: ", self.motivo_cita)
        self.input_nivel = self.creacion_formulario("Nivel_urgencia: ", self.nivel_urgencia)

        self.fecha = ttk.DateEntry(self.contenedor_formulario)
        self.fecha.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=tk.YES)       

        self.creacion_botones()
        self.tabla = self.crear_tabla()



        
        

        #crear los inputs
    def creacion_formulario(self,etiqueta, variable):
        self.contenedor_formulario = ttk.Frame(self)# crar un frame aparte
        self.contenedor_formulario.pack(fill=X,expand=YES,pady=5) #expandir formulario  y se expande en X

        contenedor_formulario_etiqueta = ttk.Label(master=self.contenedor_formulario, text=etiqueta, width=50)
        contenedor_formulario_etiqueta.pack(side=LEFT,padx=12)

        entrada_formulario = ttk.Entry(master=self.contenedor_formulario, textvariable=variable)
        entrada_formulario.pack(side=LEFT, padx=5, fill=X, expand=YES)#se expande de ambos lados


        return entrada_formulario
    

    def barra_lateral(self,texto):
        self.contenedor_formulario = ttk.Frame(self)
        self.contenedor_formulario.pack(fill=Y, expand=YES,pady=5)

        boton_formulario = ttk.Button(master=self.contenedor_formulario,text=texto, width=40)
        boton_formulario.pack(side=LEFT, padx=5, fill=Y, expand=YES)


        #creacion de botones crear y borrar
    def creacion_botones(self):
        boton_contenedor = ttk.Frame(self)
        boton_contenedor.pack(fill=X,expand=YES, pady=(15,10))

        btn_agregar = ttk.Button(
            master=boton_contenedor,
            text="Agregar Paciente",
            command=self.agregar,
            bootstyle="SUCCESS",
            width=6
        )

        btn_agregar.pack(side=RIGHT,padx=5)

        btn_editar = ttk.Button(
        master=boton_contenedor,
        text="Editar Paciente",
        command=self.editar,
        bootstyle="SUCCESS",
        width=6
        )
        btn_editar.pack(side=RIGHT, padx=5)



        
        

     
       
        

    def editar(self):
        # Obtiene los valores de la fila seleccionada en la tabla
        valores_tabla_seleccionada = self.tabla.get_rows(selected=True)[0].values

        # Verifica si hay una fila seleccionada
        if not valores_tabla_seleccionada:
            print("No hay fila seleccionada para editar.")
            return

        # Extrae los valores individuales de la fila
        id_fila = valores_tabla_seleccionada[0]
        nombre_paciente_actual = valores_tabla_seleccionada[1]
        numero_telefono_actual = valores_tabla_seleccionada[2]
        motivo_cita_actual = valores_tabla_seleccionada[3]
        fecha_actual = valores_tabla_seleccionada[4]

        # Crea un Toplevel para el diálogo de edición
        dialogo_edicion = tk.Toplevel(self.ventana)
        dialogo_edicion.title("Editar Paciente")

        # Widgets de edición
        ttk.Label(dialogo_edicion, text="ID:").pack(pady=5, anchor=tk.W)
        ttk.Label(dialogo_edicion, text=id_fila).pack(pady=5, padx=10)

        ttk.Label(dialogo_edicion, text="Nombre del paciente:", width=50).pack(pady=5, anchor=tk.W)
        entry_nombre = ttk.Entry(dialogo_edicion)
        entry_nombre.pack(pady=5, padx=10, fill=tk.X)
        entry_nombre.insert(0, nombre_paciente_actual)

        ttk.Label(dialogo_edicion, text="Número de Teléfono:").pack(pady=5, anchor=tk.W)
        entry_telefono = ttk.Entry(dialogo_edicion)
        entry_telefono.pack(pady=5, padx=10, fill=tk.X)
        entry_telefono.insert(0, numero_telefono_actual)

        ttk.Label(dialogo_edicion, text="Motivo de la Cita:").pack(pady=5, anchor=tk.W)
        entry_motivo = ttk.Entry(dialogo_edicion)
        entry_motivo.pack(pady=5, padx=10, fill=tk.X)
        entry_motivo.insert(0, motivo_cita_actual)

        ttk.Label(dialogo_edicion, text="Fecha:").pack(pady=5, anchor=tk.W)
        entry_fecha = ttk.Entry(dialogo_edicion)
        entry_fecha.pack(pady=5, padx=10, fill=tk.X)
        entry_fecha.insert(0, fecha_actual)

        # Función para guardar la edición
        def guardar_edicion():
            # Obtiene los nuevos valores desde los widgets
            nombre_paciente_editado = entry_nombre.get()
            numero_telefono_editado = entry_telefono.get()
            motivo_cita_editado = entry_motivo.get()
            fecha_editada = entry_fecha.get()

            # Actualiza la base de datos con los nuevos valores
            self.c.execute('''
                UPDATE pacientes
                SET nombre_paciente=?, numero_telefono=?, motivo_cita=?, fecha=?
                WHERE id=?
            ''', (nombre_paciente_editado, numero_telefono_editado, motivo_cita_editado, fecha_editada, id_fila))

            self.conn.commit()

            # Actualiza la tabla con los nuevos datos
            self.actualizar_tabla()

            # Cierra el diálogo de edición
            dialogo_edicion.destroy()

        # Botón para guardar la edición
        ttk.Button(dialogo_edicion, text="Guardar", command=guardar_edicion).pack(pady=10)
       
    def actualizar_tabla(self):
        self.c.execute('SELECT * FROM pacientes')
        datos_pacientes = self.c.fetchall()

        self.tabla.destroy()
        self.tabla = self.crear_tabla()

    def agregar(self, id_especifico=None):
        nombre_paciente = self.nombre_paciente.get()
        numero_telefono = self.numero_telefono.get()
        motivo_cita = self.motivo_cita.get()
        fecha_insertar = self.fecha.entry.get()

        if id_especifico:
            # Modo edición
            self.c.execute('''
                UPDATE pacientes
                SET nombre_paciente=?, numero_telefono=?, motivo_cita=?, fecha=?
                WHERE id=?
            ''', (nombre_paciente, numero_telefono, motivo_cita, fecha_insertar, id_especifico))
        else:
            # Modo inserción
            self.c.execute('''
                INSERT INTO pacientes (nombre_paciente, numero_telefono, motivo_cita, fecha)
                VALUES (?, ?, ?, ?)
            ''', (nombre_paciente, numero_telefono, motivo_cita, fecha_insertar))

        self.conn.commit()

        toast_message = "Datos actualizados" if id_especifico else "Paciente agregado"
        toast = ToastNotification(
            title=f"Paciente: {nombre_paciente}",
            message=toast_message,
            duration=3000,
        )

        toast.show_toast()

        self.actualizar_tabla()


       
    def crear_tabla(self):
         self.c.execute('SELECT * FROM pacientes')
         
         datos = self.c.fetchall()
         print(datos)
         columa_datos= [
             {"text":"ID", "stretch":False},
             {"text":"Nombre del Paciente", "stretch":False},
             {"text":"Numero de Telefono", "stretch":False},
             {"text":"Motivo de la Cita", "stretch":False},
             {"text":"Fecha", "stretch":False}

         ]

         tabla = Tableview(
            height=15,
            master=self,
            coldata=columa_datos,
            rowdata=datos,
            paginated=True,
            searchable=True,
            bootstyle=ttk.PRIMARY,
            stripecolor=(self.colors.light,None)
        )
         
         tabla.pack(expand=True)
         return tabla

    def crear_tabla_si_no_existe(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY,
                nombre_paciente TEXT,
                numero_telefono INTEGER,
                motivo_cita TEXT,
                fecha TEXT
            )
        ''')
        self.conn.commit()

    def login(self):
        root = ttk.Toplevel() #contenedor login
    
        
        def validar():
            if usuario.get() == '000' and password_usuario.get() == '000':
                root.withdraw()
                self.ventana.deiconify()
                notificacion = ToastNotification(
                    title="Contraseña y correo validados",
                    message="Haz iniciado sesion correctamente",
                    duration=3000
                )
                notificacion.show_toast()

            


       
        def create_form_entry_login(self, label, variable):
            form_field_container = ttk.Frame(root)
            form_field_container.pack(fill=X, expand=YES, pady=5)

            form_field_label = ttk.Label(master=form_field_container, text=label, width=15)
            form_field_label.pack(side=LEFT, padx=12)

            form_input = ttk.Entry(master=form_field_container, textvariable=variable)
            form_input.pack(side=LEFT, padx=5, fill=X, expand=YES)

            return form_input    
      
        label_titulo = ttk.Label(root,bootstyle=INFO,text="LOGIN",width=50)
        label_titulo.pack(fill=X,pady=10)
        label_titulo.config(font=("Georgia",20))


        usuario =ttk.StringVar(value="")
        password_usuario = ttk.StringVar(value="")

        create_form_entry_login(self,"Usuario: ",usuario)
        create_form_entry_login(self,"Contraseña : ",password_usuario)

        boton_contenedor = ttk.Frame(root)
        boton_contenedor.pack(fill=X, expand=YES, pady=(15, 10))

        login_btn = ttk.Button(
            master=boton_contenedor,
            text="LOGIN",
            command=validar,
            bootstyle=SUCCESS,
            width=6,
        )
        login_btn.pack(side=RIGHT, padx=5)




        label_registro = ttk.Label(root,bootstyle=INFO,text="REGISTRO",width=50)
        label_registro.pack(fill=X,expand=YES)
        label_registro.config(font=("Georgia",20))

        usuario_registro =ttk.StringVar(value="")
        password_usuario_registro = ttk.StringVar(value="")
        correo_electronico = ttk.StringVar(value="")
        create_form_entry_login(self,"Usuario: ",usuario_registro)
        create_form_entry_login(self,"Contraseña : ",password_usuario_registro)
        create_form_entry_login(self,"Correo: ", correo_electronico)

        boton_contenedor2 = ttk.Frame(root)
        boton_contenedor2.pack(fill=X, expand=YES, pady=(15, 10))


        register_btn = ttk.Button(
            master=boton_contenedor2,
            text="REGISTER",
            command=validar,
            bootstyle=SUCCESS,
            width=6,
        )
        register_btn.pack(side=RIGHT, padx=5)

"""
xd
"""
ventana = ttk.Window("Medicenter",'flatly', resizable=(False,False))
app = App(ventana)
ventana.mainloop()  

    
   
