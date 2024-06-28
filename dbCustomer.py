import mysql.connector
import conexion as con
import customer as ct

#Conexion con la base de datos ahora con clientes
class dbCustomers:

    def searchByName(self, clientes):
        aux=None
        try:
            self.con=con.conexion()
            self.conn=self.con.open()
            self.cursor1=self.conn.cursor()
            self.sql="select * from clientes where nombre=%s"
            self.cursor1.execute(self.sql, (clientes.getNombre(),))
            row=self.cursor1.fetchone()
            self.conn.commit()
            self.conn.close()
            if(row[0] is not None):
                aux = ct.Customer()
                aux.setCliente_id(row[0])
                aux.setUsuario_id(row[1])
                aux.setNombre(row[2])
                aux.setTelefono(row[3])
        except:
                print("Saluditos")
        return aux
        
    def nombres(self):
        self.con=con.conexion()
        self.conn=self.con.open()
        
        self.cursor1=self.conn.cursor()
        self.sql="select nombre from clientes"
        self.cursor1.execute(self.sql)
        rows=self.cursor1.fetchall()
        self.conn.commit()
        self.conn.close()
        
        nombres=list(rows)
        
        return nombres     
        
        
    def save(self,clientes):
        self.con=con.conexion()
        self.conn=self.con.open()
        self.cursor1=self.conn.cursor()
        
        self.sql="insert into clientes(cliente_id,usuario_id,nombre,telefono) values(%s,%s,%s,%s)"
        self.datos=(clientes.getCliente_id(),
                    clientes.getUsuario_id(),
                    clientes.getNombre(),
                    clientes.getTelefono())
        
        self.cursor1.execute(self.sql,self.datos)
        self.conn.commit()
        self.conn.close()
    
    def search(self, clientes):
        aux=None
        try:
            self.con=con.conexion()
            self.conn=self.con.open()
            self.cursor1=self.conn.cursor()
            self.sql="select * from clientes where cliente_id=%s"
            self.cursor1.execute(self.sql, (clientes.getCliente_id(),))
            row=self.cursor1.fetchone()
            self.conn.commit()
            self.conn.close()
            if(row[0] is not None):
                aux = ct.Customer()
                aux.setCliente_id(row[0])
                aux.setUsuario_id(row[1])
                aux.setNombre(row[2])
                aux.setTelefono(row[3])
        except:
                print("HOLA")
        return aux
        
    def edit(self, clientes):
        self.con=con.conexion()
        self.conn=self.con.open()
        self.cursor1=self.conn.cursor()
        self.sql="update clientes set nombre=%s, telefono=%s where cliente_id={}".format(clientes.getCliente_id())
        self.datos=(clientes.getNombre(), 
                    clientes.getTelefono())
            
        self.cursor1.execute(self.sql, self.datos)
        self.conn.commit()
        self.conn.close()
        
    def remove(self, clientes):
        self.con=con.conexion()
        self.conn=self.con.open()
        self.cursor1=self.conn.cursor()
        self.sql="delete from clientes where cliente_id={}".format(clientes.getCliente_id())
        self.cursor1.execute(self.sql)
        self.conn.commit()
        self.conn.close()
             
    def close(self):
        self.conn.close()