from tkinter import ttk
from tkinter import *
import sqlite3
#interfaz creada con la libreria tkinter se pueden usar otra como qt o otros framework
class Product:

    db_nombre = 'db.db'

    def __init__(self, ventana):
        #inicia la ventana
        self.wind = ventana
        self.wind.title('Productos APP')

        # creador de contenedores
        frame = LabelFrame(self.wind, text='Registrar Nuevo Producto')
        frame.grid(row=0, column=0, columnspan=3, pady=10)

        # entrada de texto
        Label(frame, text='Nombre:').grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        # entrada de texto precio
        Label(frame, text='Precio:').grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        # boton para añadir datos
        ttk.Button(frame, text='Añadir', command=self.añadir_producto).grid(row=3, columnspan=2, sticky=W+E)

        # mostrar mensajes
        self.mensaje = Label(text='', fg='red')
        self.mensaje.grid(row=3, column=0, columnspan=2, sticky=W+E)
        
        # tabla
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0,columnspan=2)
        self.tree.heading('#0', text='Nombre', anchor=CENTER)
        self.tree.heading('#1', text='Precio', anchor=CENTER)

        # botones borrar
        ttk.Button(text='Borrar',command=self.eliminar_producto).grid(row=5, column=0, sticky=W+E)
        ttk.Button(text='Editar',command=self.editar).grid(row=5, column=1, sticky=W+E)
        
        # llenado de tabla
        self.obtener_producto()

    #funcion que realiza las consultas a la bd
    def consultas(self,consulta,parametros=()):
        with sqlite3.connect(self.db_nombre) as conn:
            cursor = conn.cursor()
            result = conn.execute(consulta,parametros)
            conn.commit()
        return result

    def obtener_producto(self):
        # borrando tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # consultando
        consulta = 'SELECT * FROM producto ORDER BY nombre DESC'
        db_rows = self.consultas(consulta)
        # rellenado datos
        for row in db_rows:
            self.tree.insert('',0,text=row[1],values=row[2])
    
    #validando datos
    def validar(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def añadir_producto(self):
        if self.validar():
            consulta = 'INSERT INTO producto VALUES(NULL,?,?)'
            parametros = (self.name.get(), self.price.get())
            self.consultas(consulta, parametros)
            self.mensaje['text'] = 'producto {} añadido'.format(
                self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.mensaje['text'] = 'no hay datos de producto'
        self.obtener_producto()

    def eliminar_producto(self):
        self.mensaje['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text']='seleccionar un producto'
            return
        self.mensaje['text']=''

        nombre=self.tree.item(self.tree.selection())['text']
        consulta='DELETE FROM producto WHERE nombre=?'
        
        self.consultas(consulta,(nombre, ))
        self.mensaje['text']='producto {} eliminado'.format(nombre)
        self.obtener_producto()

    def editar(self):
        self.mensaje['text']=''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.mensaje['text']='seleccionar un producto'
            return
        nombreant=self.tree.item(self.tree.selection())['text']
        precioant=self.tree.item(self.tree.selection())['values'][0]
        self.ventanaeditar=Toplevel()
        self.ventanaeditar.title='Editar Producto'

        #nombre antigua en ventana
        Label(self.ventanaeditar,text='Nombre:').grid(row=0,column=1)
        Entry(self.ventanaeditar,textvariable=StringVar(self.ventanaeditar,value=nombreant),state='readonly').grid(row=0,column=2)
        #editar nombre
        Label(self.ventanaeditar,text='Nuevo Nombre:').grid(row=1,column=1)
        nuevonombre=Entry(self.ventanaeditar)
        nuevonombre.grid(row=1,column=2)
        #precio antiguo en ventana
        Label(self.ventanaeditar,text='Precio:').grid(row=4,column=1)
        Entry(self.ventanaeditar,textvariable=StringVar(self.ventanaeditar,value=precioant),state='readonly').grid(row=4,column=2)
        #editar precio
        Label(self.ventanaeditar,text='Nuevo Precio:').grid(row=5,column=1)
        nuevoprecio=Entry(self.ventanaeditar)
        nuevoprecio.grid(row=5,column=2)
        #boton para guardar cambios
        ttk.Button(self.ventanaeditar,text='Guardar',command=lambda: self.editardatos(nuevonombre.get(),nuevoprecio.get(),nombreant,precioant)).grid(row=6,column=1,columnspan=2,sticky=W+E)
        #self.ventanaeditar.mainloop()

    def editardatos(self,nuevonombre,nuevoprecio,nombreant,precioant):
        consulta='UPDATE producto SET nombre=?,precio=? WHERE nombre=? AND precio=?'
        parametros=(nuevonombre,nuevoprecio,nombreant,precioant)
        self.consultas(consulta,parametros)
        self.ventanaeditar.destroy()
        self.mensaje['text']='producto {} ha sido añadido'.format(nuevonombre)
        self.obtener_producto()

if __name__ == '__main__':
    ventana = Tk()
    application = Product(ventana)
    ventana.mainloop()