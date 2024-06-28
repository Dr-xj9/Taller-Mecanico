import dbUsuario
import dbCustomer
import dbVehiculo
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
import usuario as user
import customer as ct
import vehiculo as vh
import conexion as con

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        
        #Labels que aparecen antes de la entrada
        self.seccion_usuario = tk.Label(root, text="UserName")
        self.seccion_password = tk.Label(root, text="Password")
        
        #Entrada del usuario se almacenan aqui
        self.entrada_usuario = tk.Entry(root)
        self.entrada_password = tk.Entry(root, show='*')
        
        #Botones
        self.boton_acceder = tk.Button(root, text="Login", command=self.logear)
        
        #posiciones
        self.seccion_usuario.grid(row=0, column=0, padx=25, pady=20)
        self.seccion_password.grid(row=1, column=0, padx=25, pady=20)
        
        self.entrada_usuario.grid(row=0, column=1, padx=25, pady=8)
        self.entrada_password.grid(row=1, column=1, padx=25, pady=8)
        
        self.boton_acceder.grid(row=2, column=0, columnspan=2, pady=20)
        
    #Esta funcion se encarga de retornar los datos de entrada de usuario para su validacion    
    def logear(self):
        username = self.entrada_usuario.get()
        password = self.entrada_password.get()
        
        u = user.usuario()
        u.setUserName(username)
        u.setPassword(password)
        
        db = dbUsuario.dbUsuario()
        data = db.Autentificar(u)
        if(data is None):
            messagebox.showinfo("Error", "Verifique que el usuario y contraseña sean correctos")
        else:
            self.root.withdraw()
            self.menuPrincipal()

    def menuPrincipal(self):
        self.nueva_ventana = tk.Toplevel(self.root, width=500)
        self.nueva_ventana.title("Usuario")
        
        self.opcion_seleccionada = tk.StringVar()

        # Crear y configurar el menú desplegable
        opciones = ["Usuarios", "Clientes", "Vehiculos", "Salir"]
        self.menu_desplegable = tk.OptionMenu(self.nueva_ventana, self.opcion_seleccionada, *opciones)
        self.menu_desplegable.grid(column=0, row=0)

        # Crear un contenedor para el contenido central
        self.centro_frame = tk.Frame(self.nueva_ventana, bg="lightgray", width=500, height=300)
        self.centro_frame.grid(column=1, row = 1)
        
        # Configurar un rastreador de cambios en el menú desplegable
        self.opcion_seleccionada.trace_add("write", self.actualizar)
 
    def actualizar(self, *args):
        opcion = self.opcion_seleccionada.get()
        self.mostrar_contenido(opcion)
        
    def mostrar_contenido(self, opcion):
        # Limpiar el contenido central actual
        for widget in self.centro_frame.winfo_children():
            widget.destroy()

        # Mostrar el nuevo contenido según la opción seleccionada
        if opcion == "Usuarios":
            self.menuUsuario()
        elif opcion == "Salir":
            self.salir()
        elif opcion == "Clientes":
            self.menuCliente()
        elif opcion == "Vehiculos":
            self.menuVehiculos()
        
    def menuUsuario(self):
        label_b=tk.Label(self.centro_frame, text="Buscar ID:")
        label_b.grid(row=0, column=0, padx=5, pady=15, sticky="e")
        
        self.entry_b = tk.Entry(self.centro_frame)
        self.entry_b.grid(row=0, column=1, padx=5, pady=5)
        entrada_b=self.entry_b.get()
        self.boton_buscar = tk.Button(self.centro_frame, text="Buscar", command=lambda:self.buscar(campos_entries, self.entry_b))
        self.boton_buscar.grid(row=0, column=2, columnspan=2, pady=10)
        
        #Campos Llenables por entrada
        campos = ["Usuario ID", "Nombre", "User Name", "Password"]
        campos_entries = {}
        
        for i, campo in enumerate(campos):
            label = tk.Label(self.centro_frame, text=f"{campo}:")
            label.grid(row=i+1, column=0, padx=5, pady=5, sticky="e")

            entry_var = tk.StringVar()
            self.entry = tk.Entry(self.centro_frame, textvariable=entry_var)
            self.entry.grid(row=i+1, column=1, padx=5, pady=5)
            campos_entries[campo] = entry_var
        
        #Perfil
        labelPerfil = tk.Label(self.centro_frame, text="Perfil:")
        labelPerfil.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        
        perfil= tk.StringVar()
        self.combo = ttk.Combobox(self.centro_frame, textvariable=perfil)
        self.combo['values'] = ("Mecanico", "Secretario", "Cliente", "Administrador")
        self.combo.grid(row=5, column = 1, padx=5, pady=5)
        campos_entries["Perfil"] = perfil
                  
        # Botón Guardar
        self.boton_obtener_datos = tk.Button(self.centro_frame, text="Guardar", command=lambda:self.guardar(campos_entries))
        self.boton_obtener_datos.grid(row=len(campos)+2, column=0, columnspan=2, pady=10)

        # Boton para reiniciar
        self.boton_reiniciar_campos = tk.Button(self.centro_frame, text="Nuevo", command=lambda:self.reiniciar_campos(campos_entries))
        self.boton_reiniciar_campos.grid(row=len(campos)+2, column=2, columnspan=2, pady=10)
        
        # Boton editar
        self.boton_editar = tk.Button(self.centro_frame, text="Editar", command=lambda:self.editar(campos_entries))
        self.boton_editar.grid(row=len(campos)+2, column=6, columnspan=2, pady=10)
        
        # Boton Eliminar
        self.boton_eliminar = tk.Button(self.centro_frame, text="Eliminar", command=lambda:self.eliminar(self.entry_b, campos_entries))
        self.boton_eliminar.grid(row=len(campos)+2, column=8, columnspan=2, pady=10)
        
        self.boton_cancelar = tk.Button(self.centro_frame, text="Cancelar", command=lambda: self.cancelar(campos_entries)).grid(row=len(campos)+2, column=10, columnspan=2, pady=10)
        
    def habilitar_entradas(self):
        # Cambiar el estado de todas las entradas a NORMAL
        for widget in self.centro_frame.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.config(state=tk.NORMAL)

    def deshabilitar_entradas(self):
        # Cambiar el estado de todas las entradas a DISABLED
        for widget in self.centro_frame.winfo_children():
            if isinstance(widget, tk.Entry):
                widget.config(state=tk.DISABLED)
    
    #NO TOCAR NADA DE AQUI
    def cancelar(self, campos_entries):
        self.boton_reiniciar_campos.config(state="normal")
        self.boton_eliminar.config(state="normal")
        self.boton_editar.config(state = "normal")
        self.boton_obtener_datos.config(state="normal")
        self.boton_buscar.config(state="normal")
        self.habilitar_entradas()
        for entry_var in campos_entries.values():
            entry_var.set("") 
        
    def reiniciar_campos(self, campos_entries):
        self.boton_reiniciar_campos.config(state="disabled")
        self.boton_eliminar.config(state="disabled")
        self.boton_editar.config(state = "disabled")
        self.boton_buscar.config(state = "disabled")
        self.habilitar_entradas()
        for entry_var in campos_entries.values():
           entry_var.set("")
        
    
    def guardar(self, campos_entries):
        estadoBotonEditar = self.boton_editar.cget("state")
        usuarioInstancia = user.usuario()
        
        for campo, variable in campos_entries.items():
            valores = variable.get()
            if(campo == "Usuario ID"):
                v = valores
                usuarioInstancia.setUsuario_id(valores)
            elif(campo == "Nombre"):
                usuarioInstancia.setNombre(valores)
            elif(campo == "User Name"):
                usuarioInstancia.setUserName(valores)
            elif(campo == "Password"):
                usuarioInstancia.setPassword(valores)
            elif(campo == "Perfil"):
                usuarioInstancia.setPerfil(valores)          
        db = dbUsuario.dbUsuario()
        if(estadoBotonEditar == "disabled"): #si vamos a guardar
            if(db.save(usuarioInstancia)):
                messagebox.showinfo("Correcto", "datos guardados correctamente")
            else:
                messagebox.showinfo("Error", "ID: "+ v +" ya se encuentra registrado")
            self.boton_reiniciar_campos.config(state="normal")
            self.boton_eliminar.config(state="normal")
            self.boton_buscar.config(state="normal")
            self.boton_editar.config(state = "normal")
            self.deshabilitar_entradas()
        elif(estadoBotonEditar == "normal"): #si vamos a editar
            db.edit(usuarioInstancia)
            messagebox.showinfo("Correcto", "datos guardados correctamente")
         
        for entry_var in campos_entries.values():
          entry_var.set("")
        self.boton_reiniciar_campos.config(state="normal")
    
    def buscar(self, campos_entries, campoBusqueda):
        self.deshabilitar_entradas()
        self.boton_obtener_datos.config(state="disabled")
        self.boton_reiniciar_campos.config(state="disabled")
        
        #Instanciar campos
        db = dbUsuario.dbUsuario()
        usuarioInstancia = user.usuario()
        
        #Settear el id a buscar con la clase usuario
        idBuscar=campoBusqueda.get()
        usuarioInstancia.setUsuario_id(idBuscar)
        
        #Buscar en la base de datos
        usuarioEncontrado = db.search(usuarioInstancia)
        
        #Si se encontró
        if(usuarioEncontrado is not None):
            for campo, variable in campos_entries.items():
                if(campo == "Usuario ID"):
                    variable.set(usuarioEncontrado.getUsuario_id())
                elif(campo == "Nombre"):
                    variable.set(usuarioEncontrado.getNombre())
                elif(campo == "User Name"):
                    variable.set(usuarioEncontrado.getUserName())
                elif(campo == "Password"):
                    variable.set(usuarioEncontrado.getPassword())
                elif(campo == "Perfil"):
                    variable.set(usuarioEncontrado.getPerfil())
        else:
            messagebox.showinfo("Error", "Usuario no encontrado en la base de datos")
    
    def editar(self, campos_entries):
        self.habilitar_entradas()
        self.boton_obtener_datos.config(state="normal")
        
    def eliminar(self, campoRecibido, campos_entries):
        idEliminar = campoRecibido.get()
        
        #Setear el objeto usuario
        usuarioIdEliminar = user.usuario()
        usuarioIdEliminar.setUsuario_id(idEliminar)
        
        #Setear la conexion con la DB y remover
        database = dbUsuario.dbUsuario()
        database.remove(usuarioIdEliminar)
        messagebox.showinfo("Correcto", "Usuario eliminado con exito")
        for entry_var in campos_entries.values():
          entry_var.set("")
    
    
    def salir(self):
        self.root.destroy()
    
    # Menú de la seccion clientes
    def menuCliente(self):
        self.nueva_ventana.title("Cliente")
        
        #Varibles para mantener control de las salidas
        self.variableBusqueda = tk.StringVar()
        self.variableID = tk.StringVar()
        self.variableUserName = tk.StringVar()
        self.variableIDForaneo = tk.StringVar()
        self.variableNombreCliente = tk.StringVar()
        self.variableTelefono = tk.StringVar()
        
        #Label y entrada
        labelBuscar = tk.Label(self.centro_frame, text="Entrada ID").grid(row=0, column=0, padx=5)
        self.entradaBusqueda = tk.Entry(self.centro_frame, textvariable=self.variableBusqueda)
        self.entradaBusqueda.grid(row=0, column=1, padx=5)
        #Boton
        self.boton_buscar_cliente = tk.Button(self.centro_frame,text="Buscar", command=self.buscarCliente)
        self.boton_buscar_cliente.grid(row=0, column=2, padx=5)
        
        labelId = tk.Label(self.centro_frame, text="ID:").grid(row=1, column=0, padx=5, pady=8)
        self.entradaId = tk.Entry(self.centro_frame, textvariable=self.variableID)
        self.entradaId.grid(row=1, column=1, padx=5, pady=8)
        
        #Recordatorio ESTOS CAMPOS SON FORANEOS
        labelUserName = tk.Label(self.centro_frame, text="User Name").grid(row=2, column=0, padx=5, pady=8)
        
        self.entradaUserName = tk.Entry(self.centro_frame, textvariable=self.variableUserName)
        self.entradaUserName.grid(row=2, column=1, padx=5, pady=8)
        self.entradaUserName.config(state=tk.DISABLED)
        
        self.entradaIDForaneo = tk.Entry(self.centro_frame, textvariable=self.variableIDForaneo)
        self.entradaIDForaneo.grid(row=2, column=2, sticky="e")
        self.entradaIDForaneo.config(state=tk.DISABLED)
        
        self.variableUserName.set(self.entrada_usuario.get())
        idObtenido = self.obtenerIDUsername()
        self.variableIDForaneo.set(idObtenido)
        #Fin de los campos foraneos
        
        labelNombre = tk.Label(self.centro_frame, text="Nombre del Cliente").grid(row=3, column=0, padx=6, pady=8)
        self.entradaNombre = tk.Entry(self.centro_frame, textvariable=self.variableNombreCliente)
        self.entradaNombre.grid(row=3, column=1, padx=5, pady=8)
        
        labelTelefono = tk.Label(self.centro_frame, text="Telefono").grid(row=4, column=0, padx=5, pady=8)
        self.entradaTelefono= tk.Entry(self.centro_frame, textvariable=self.variableTelefono)
        self.entradaTelefono.grid(row=4, column=1, padx=5, pady=8)
        
        #Botones
        self.boton_guardar = tk.Button(self.centro_frame, text="Guardar",command=self.guardarCliente)
        self.boton_guardar.grid(row=6, column=2)
        self.boton_nuevo = tk.Button(self.centro_frame, text="Nuevo", command=self.nuevoCliente)
        self.boton_nuevo.grid(row=6, column=0, columnspan=3)
        self.boton_editar = tk.Button(self.centro_frame, text="Editar", command=self.editarCliente)
        self.boton_editar.grid(row=6, column=6)
        self.boton_cancelar = tk.Button(self.centro_frame, text="Cancelar", command=self.cancelarCliente)
        self.boton_cancelar.grid(row=6, column=4)
        
        #Edo inicial
        self.deshabilitarEntradasClientes()
        
    def obtenerIDUsername(self):
        baseD= dbUsuario.dbUsuario()
        us = user.usuario()
        
        userNlogin = self.entrada_usuario.get()
        us.setUserName(userNlogin)
        
        resultado = baseD.searchID(us)
        if(resultado is not None):
            return resultado.getUsuario_id()
        else:
            print("No se encontraron resultados")
            return None
    
    def deshabilitarEntradasClientes(self):
        self.entradaId.config(state=tk.DISABLED)
        self.entradaNombre.config(state=tk.DISABLED)
        self.entradaTelefono.config(state=tk.DISABLED)
    
    def habilitarEntradasClientes(self):
        self.entradaId.config(state=tk.NORMAL)
        self.entradaNombre.config(state=tk.NORMAL)
        self.entradaTelefono.config(state=tk.NORMAL)
        
    def vaciarCampos(self):
        self.variableBusqueda.set("")
        self.variableID.set("")
        self.variableNombreCliente.set("")
        self.variableTelefono.set("")
    
    def cancelarCliente(self):
        self.entradaBusqueda.config(state=tk.NORMAL)
        self.deshabilitarEntradasClientes()
        self.boton_buscar_cliente.config(state="normal")
        self.boton_nuevo.config(state="normal")
        self.boton_guardar.config(state="normal")
        self.boton_editar.config(state="normal")
        
        self.vaciarCampos()
        
    def nuevoCliente(self):
        self.habilitarEntradasClientes()
        self.entradaBusqueda.config(state=tk.NORMAL)
        self.boton_buscar_cliente.config(state="disabled")
        self.boton_nuevo.config(state="disabled")
        self.boton_editar.config(state="disabled")
        
    def guardarCliente(self):
        base = dbCustomer.dbCustomers()
        clienteObjeto = ct.Customer()
        
        clienteObjeto.setCliente_id(self.variableID.get())
        clienteObjeto.setNombre(self.variableNombreCliente.get())
        clienteObjeto.setTelefono(self.variableTelefono.get())
        clienteObjeto.setUsuario_id(self.variableIDForaneo.get())
        
        estadoBotonEditar = self.boton_editar.cget("state")
        if(estadoBotonEditar == "disabled"):
            base.save(clienteObjeto)
            messagebox.showinfo("Guardado", "Cliente registrado con exito")
        else:
            base.edit(clienteObjeto)
            messagebox.showinfo("Guardado", "Nuevos datos registrados con exito")
        self.vaciarCampos()    
        
    def editarCliente(self):
        self.entradaNombre.config(state=tk.NORMAL)
        self.entradaTelefono.config(state=tk.NORMAL)
        self.boton_guardar.config(state="normal")
        
    def buscarCliente(self):
        self.deshabilitarEntradasClientes()
        self.boton_nuevo.config(state="disabled")
        self.boton_guardar.config(state="disabled")
        
        cliente = ct.Customer()
        usuario = user.usuario()
        
        base = dbCustomer.dbCustomers()
        baseUsuario = dbUsuario.dbUsuario()
        
        clienteID = self.variableBusqueda.get()
        cliente.setCliente_id(clienteID)
        
        datosRecibidos = base.search(cliente)
        if(datosRecibidos is not None):
           self.variableID.set(datosRecibidos.getCliente_id())
           self.variableIDForaneo.set(datosRecibidos.getUsuario_id())
           self.variableNombreCliente.set(datosRecibidos.getNombre())
           self.variableTelefono.set(datosRecibidos.getTelefono())
        else:
            messagebox.showinfo("Error", "Cliente no encontrado")
    
    def menuVehiculos(self):
        self.nueva_ventana.title("Vehiculos")
        
        #Variables
        self.nombre_cliente_box = tk.StringVar()
        self.vehiculo_id = tk.StringVar()
        self.matricula = tk.StringVar()
        self.marca = tk.StringVar()
        self.modelo = tk.StringVar()
        self.vehiculo_id_buscar = tk.StringVar()
        
        #Combobox clientes
        label_cliente_nombre = tk.Label(self.centro_frame, text="Seleccione Cliente: ").grid(row=0, column=0)
        nombres_clientes = self.nombresClientes() #Util
        self.combo_clientes = ttk.Combobox(self.centro_frame, textvariable=self.nombre_cliente_box)
        self.combo_clientes['values'] = nombres_clientes
        self.combo_clientes.grid(row=0, column = 1, padx=5)
        
        label_busqueda_id = tk.Label(self.centro_frame, text="Buscar Vehiculo: ").grid(row=0, column=2, padx=10)
        self.vid = tk.Entry(self.centro_frame, textvariable=self.vehiculo_id_buscar)
        self.vid.grid(row=0, column=3, padx=5)
        
        self.boton_buscar_vehiculo = tk.Button(self.centro_frame, text="Buscar", command=self.buscarVehiculo)
        self.boton_buscar_vehiculo.grid(row=0, column=4, padx=5)
        
        label_vehiculo = tk.Label(self.centro_frame, text="Vehiculo ID:").grid(row=1, column=0, pady=10)
        self.vehiculo_id_entry = tk.Entry(self.centro_frame, textvariable=self.vehiculo_id)
        self.vehiculo_id_entry.grid(row=1, column=1, padx=5)
        
        label_matricula = tk.Label(self.centro_frame, text="Matricula").grid(row=2, column=0, pady=10)
        self.matricula_entry = tk.Entry(self.centro_frame, textvariable=self.matricula)
        self.matricula_entry.grid(row=2, column=1, padx=5)
        
        label_marca = tk.Label(self.centro_frame, text="Marca").grid(row=3, column=0, pady=10)
        self.marca_entry = tk.Entry(self.centro_frame, textvariable=self.marca)
        self.marca_entry.grid(row=3, column=1, padx=5)
        
        label_modelo = tk.Label(self.centro_frame, text="Modelo").grid(row=4, column=0, pady=10)
        self.modelo_entry = tk.Entry(self.centro_frame, textvariable=self.modelo)
        self.modelo_entry.grid(row=4, column=1, padx=5)
        
        self.boton_nuevo_vehiculo = tk.Button(self.centro_frame, text="Nuevo", command=self.nuevoVehiculo)
        self.boton_nuevo_vehiculo.grid(row=5, column=0, pady=20)
        
        self.boton_salvar_vehiculo = tk.Button(self.centro_frame, text="Guardar", command=self.guardarVehiculo)
        self.boton_salvar_vehiculo.grid(row=5, column=1, pady=20)
        
        self.boton_cancelar_vehiculo = tk.Button(self.centro_frame, text="Cancelar", command=self.cancelarVehiculo)
        self.boton_cancelar_vehiculo.grid(row=5, column=2, pady=20)
        
        self.boton_editar_vehiculo = tk.Button(self.centro_frame, text="Editar", command=self.editarVehiculo)
        self.boton_editar_vehiculo.grid(row=5, column=3, pady=20)
        
        self.boton_borrar_vehiculo = tk.Button(self.centro_frame, text="Remover", command=self.removerVehiculo)
        self.boton_borrar_vehiculo.grid(row=5, column=4, pady=20)
        
        self.inicio() #Edo inicial
        
    def nombresClientes(self):
        baseExtraer = dbCustomer.dbCustomers()
        nomClientes = baseExtraer.nombres()
        return nomClientes
    
    def nuevoVehiculo(self):
        self.vehiculo_id_entry.config(state=tk.NORMAL)
        self.matricula_entry.config(state=tk.NORMAL)
        self.marca_entry.config(state=tk.NORMAL)
        self.modelo_entry.config(state=tk.NORMAL)
        self.boton_salvar_vehiculo.config(state="normal")
        self.boton_buscar_vehiculo.config(state="disabled")
        
    def inicio(self):
        self.vehiculo_id_entry.config(state=tk.DISABLED)
        self.matricula_entry.config(state=tk.DISABLED)
        self.marca_entry.config(state=tk.DISABLED)
        self.modelo_entry.config(state=tk.DISABLED)
        
        self.boton_editar_vehiculo.config(state="disabled")
        self.boton_borrar_vehiculo.config(state="disabled")
        self.boton_salvar_vehiculo.config(state="disabled")
        self.boton_nuevo_vehiculo.config(state="normal")
        self.boton_buscar_vehiculo.config(state="normal")
        
    def cancelarVehiculo(self):
        self.inicio()
        self.vacio()
        
        
    def buscarVehiculo(self):
        self.boton_editar_vehiculo.config(state="normal")
        self.boton_borrar_vehiculo.config(state="normal")
        
        self.boton_nuevo_vehiculo.config(state="disabled")
        self.boton_salvar_vehiculo.config(state="disabled")
        
        self.vehiculo_id_entry.config(state=tk.DISABLED)
        self.matricula_entry.config(state=tk.DISABLED)
        self.marca_entry.config(state=tk.DISABLED)
        self.modelo_entry.config(state=tk.DISABLED)
        
        baseClientes = dbCustomer.dbCustomers()
        baseAutos = dbVehiculo.dbVehiculos()
        vehiculoObjeto = vh.Vehiculo()
        clienteObjeto = ct.Customer()
        vehiculoObjeto.set_vehiculo_id(self.vid.get())
        
        resBase = baseAutos.search(vehiculoObjeto)
        
        if(resBase is not None):
            
            clienteObjeto.setCliente_id(resBase.get_cliente_id())  
            Sacarnombre = baseClientes.search(clienteObjeto)
            
            self.nombre_cliente_box.set(Sacarnombre.getNombre())
            self.vehiculo_id.set(resBase.get_vehiculo_id())
            self.marca.set(resBase.get_marca())
            self.modelo.set(resBase.get_modelo())
            self.matricula.set(resBase.get_matricula())
        else:
            messagebox.showinfo("ERROR", "Vehiculo No Encontrado")
            self.inicio()
            self.vacio()
        
    def removerVehiculo(self):
        baseAutos = dbVehiculo.dbVehiculos()
        Objtemp = vh.Vehiculo()
        Objtemp.set_vehiculo_id(self.vehiculo_id.get())
        baseAutos.remove(Objtemp)
        messagebox.showinfo("Eliminar", "Vehiculo Eliminado")
        self.inicio()
        self.vacio()
        
    def editarVehiculo(self):
        self.matricula_entry.config(state=tk.NORMAL)
        self.marca_entry.config(state=tk.NORMAL)
        self.modelo_entry.config(state=tk.NORMAL)
        self.boton_salvar_vehiculo.config(state="normal")
        
    def guardarVehiculo(self):
        #Objetos de las bases
        base = dbVehiculo.dbVehiculos()
        baseClientes = dbCustomer.dbCustomers()
        
        vehiculoObjeto = vh.Vehiculo()
        clienteObjeto = ct.Customer()
        
        clienteObjeto.setNombre(self.nombre_cliente_box.get())
        objetoRecibido = baseClientes.searchByName(clienteObjeto)
        
        vehiculoObjeto.set_cliente_id(objetoRecibido.getCliente_id())
        vehiculoObjeto.set_vehiculo_id(self.vehiculo_id.get())
        vehiculoObjeto.set_matricula(self.matricula.get())
        vehiculoObjeto.set_marca(self.marca.get())
        vehiculoObjeto.set_modelo(self.modelo.get())
        
        estado_btEditar=self.boton_editar_vehiculo.cget("state")
        if(estado_btEditar == "disabled"):
            base.save(vehiculoObjeto)
            messagebox.showinfo("Guardado", "Vehiculo Registrado")
        else:
            base.edit(vehiculoObjeto)
            messagebox.showinfo("Editado", "Cambios Guardados")
        
        self.inicio()
        self.vacio()
            
    def vacio(self):
        self.vehiculo_id.set("")
        self.matricula.set("")
        self.marca.set("")
        self.modelo.set("")
        self.vehiculo_id_buscar.set("")
        
    def menuPiezas(self):
        pass
        
        
        
if (__name__== "__main__"):
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()