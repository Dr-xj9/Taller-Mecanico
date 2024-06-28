class Customer:
    def __init__(self):
        cliente_id=0
        usuario_id=0
        nombre=""
        telefono=""
    #setter
    def setCliente_id(self, clienteReferencia):
        self.cliente_id=clienteReferencia
    def setUsuario_id(self, UsuarioReferencia):
        self.usuario_id=UsuarioReferencia
    def setNombre(self, nombreRef):
        self.nombre=nombreRef
    def setTelefono(self, teleRef):
        self.telefono = teleRef
    #getter
    def getCliente_id(self):
        return self.cliente_id
    def getUsuario_id(self):
        return self.usuario_id
    def getNombre(self):
        return self.nombre
    def getTelefono(self):
        return self.telefono
    