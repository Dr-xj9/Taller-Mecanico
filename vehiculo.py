#la clase vehiculo así es

class Vehiculo:
    def __init__(self):
        self._vehiculo_id = 0
        self._cliente_id = 0
        self._matricula = ""
        self._marca = ""
        self._modelo = 0
    
    #setter    
    def set_vehiculo_id(self, vehiculo_id):
        self._vehiculo_id = vehiculo_id

    def set_cliente_id(self, cliente_id):
        self._cliente_id = cliente_id
    
    def set_matricula(self, matricula):
        self._matricula = matricula
    
    def set_marca(self, marca):
        self._marca = marca
        
    def set_modelo(self, modelo):
        self._modelo = modelo

    #getter
    def get_vehiculo_id(self):
        return self._vehiculo_id
    
    def get_cliente_id(self):
        return self._cliente_id

    def get_matricula(self):
        return self._matricula

    def get_marca(self):
        return self._marca

    def get_modelo(self):
        return self._modelo
