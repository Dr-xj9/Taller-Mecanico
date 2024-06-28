import mysql.connector
import vehiculo as vh
import conexion as con

#class base de datos vehiculos
class dbVehiculos:
    def save(self,vehiculo):
        self.con=con.conexion()
        self.conn=self.con.open()
        self.cursor1=self.conn.cursor()
        
        self.sql="insert into vehiculos(vehiculo_id, matricula, marca, modelo, cliente_id) values(%s,%s,%s,%s,%s)"
        self.datos=(vehiculo.get_vehiculo_id(),
                    vehiculo.get_matricula(),
                    vehiculo.get_marca(),
                    vehiculo.get_modelo(),
                    vehiculo.get_cliente_id())
        
        self.cursor1.execute(self.sql,self.datos)
        self.conn.commit()
        self.conn.close()
    
    def search(self, vehiculos):
        aux=None
        try:
            self.con=con.conexion()
            self.conn=self.con.open()
            self.cursor1=self.conn.cursor()
            self.sql="select * from vehiculos where vehiculo_id=%s"
            self.cursor1.execute(self.sql, (vehiculos.get_vehiculo_id(),))
            row=self.cursor1.fetchone()
            self.conn.commit()
            self.conn.close()
            if(row[0] is not None):
                aux = vh.Vehiculo()
                aux.set_vehiculo_id(row[0])
                aux.set_matricula(row[1])
                aux.set_marca(row[2])
                aux.set_modelo(row[3])
                aux.set_cliente_id(row[4])
        except:
                print("Saluditos")
        return aux
        
    def edit(self, vehiculos):
        self.con=con.conexion()
        self.conn=self.con.open()
        self.cursor1=self.conn.cursor()
        self.sql="update vehiculos set matricula=%s, marca=%s, modelo=%s where vehiculo_id={}".format(vehiculos.get_vehiculo_id())
        self.datos=(vehiculos.get_matricula(),
                    vehiculos.get_marca(), 
                    vehiculos.get_modelo())
            
        self.cursor1.execute(self.sql, self.datos)
        self.conn.commit()
        self.conn.close()
        
    def remove(self, vehiculos):
        self.con=con.conexion()
        self.conn=self.con.open()
        self.cursor1=self.conn.cursor()
        self.sql="delete from vehiculos where vehiculo_id={}".format(vehiculos.get_vehiculo_id())
        self.cursor1.execute(self.sql)
        self.conn.commit()
        self.conn.close()
             
    def close(self):
        self.conn.close()