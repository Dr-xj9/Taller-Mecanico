import mysql.connector
import usuario as user
import conexion as con

class dbUsuario:
    def save(self,usuario):
      try:
        self.con=con.conexion()
        self.conn=self.con.open()
        self.cursor1=self.conn.cursor()
        self.sql="insert into usuarios(usuario_id,nombre,username,password,perfil) values(%s,%s,%s,%s,%s)"
        self.datos=(usuario.getUsuario_id(),
                    usuario.getNombre(),
                    usuario.getUserName(),
                    usuario.getPassword(),
                    usuario.getPerfil())
        self.cursor1.execute(self.sql,self.datos)
        self.conn.commit()
        self.conn.close()
      except:
        print("Error Usuario Existente")
        return False
      return True
    
    def searchID(self, usuario):
        aux=None
        try:
            self.con=con.conexion()
            self.conn=self.con.open()
            self.cursor1=self.conn.cursor()
            self.sql="select * from usuarios where username=%s"
            self.cursor1.execute(self.sql, (usuario.getUserName(),))  # Pasar los parámetros como una tupla
            row=self.cursor1.fetchone()
            self.conn.commit()
            self.conn.close()
            if(row[0] is not None):
                aux = user.usuario()
                aux.setUsuario_id(row[0])
                aux.setNombre(row[1])
                aux.setUserName(row[2])
                aux.setPassword(row[3])
                aux.setPerfil(row[4])
            
        except:
                print("ERROR")
        return aux
        
    def search(self, usuario):
        aux=None
        try:
            self.con=con.conexion()
            self.conn=self.con.open()
            self.cursor1=self.conn.cursor()
            self.sql="select * from usuarios where usuario_id=%s"
            self.cursor1.execute(self.sql, (usuario.getUsuario_id(),))  # Pasar los parámetros como una tupla
            row=self.cursor1.fetchone()
            self.conn.commit()
            self.conn.close()
            if(row[0] is not None):
                aux = user.usuario()
                aux.setUsuario_id(row[0])
                aux.setNombre(row[1])
                aux.setUserName(row[2])
                aux.setPassword(row[3])
                aux.setPerfil(row[4])
            
        except:
                print("Saluditos")
        return aux
    
    def edit(self,usuario):
        self.con=con.conexion()
        self.conn=self.con.open()
        self.cursor1=self.conn.cursor()
        self.sql="update usuarios set nombre=%s, username=%s, perfil=%s where usuario_id={}".format(usuario.getUsuario_id())
        self.datos=(usuario.getNombre(), 
                    usuario.getUserName(),
                    usuario.getPerfil())
        self.cursor1.execute(self.sql, self.datos)
        self.conn.commit()
        self.conn.close()
    
    def remove(self, usuario):
        self.con=con.conexion()
        self.conn=self.con.open()
        self.cursor1=self.conn.cursor()
        self.sql="delete from usuarios where usuario_id={}".format(usuario.getUsuario_id())
        self.cursor1.execute(self.sql)
        self.conn.commit()
        self.conn.close()
    
    def getMaxId(self):
        id=1
        self.con=con.conexion()
        self.conn=self.con.open()
        self.cursor1 = self.conn.cursor()
        self.sql = "select max(usuario_id) as id from usuarios"
        self.cursor1.execute(self.sql)
        row=self.cursor1.fetchone()
        self.conn.commit()
        self.conn.close()
    
    def Autentificar(self, usuario):
        aux = None
        try:
            self.con = con.conexion()
            self.conn = self.con.open()
            self.cursor1 = self.conn.cursor()
            self.sql = "SELECT * FROM usuarios WHERE username = %s"
            self.cursor1.execute(self.sql, (usuario.getUserName(),))
            row = self.cursor1.fetchone()
            self.conn.commit()
            self.conn.close()
            if row[0] is not None:
                if usuario.getPassword() == row[3]:
                    aux = user.usuario()
                    aux.setUsuario_id(int(row[0]))
                    aux.setNombre(row[1])
                    aux.setUserName(row[2])
                    aux.setPassword(row[3])
                    aux.setPerfil(row[4])
        except Exception as e:
            print(f"Error: {e}")
        return aux
