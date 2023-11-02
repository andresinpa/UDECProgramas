
from flask_login import UserMixin
from werkzeug.security import check_password_hash

class Usuario(UserMixin):
    def __init__(self, id, email, password, nombres=""):
        self.id = id
        self.email = email
        self.password = password
        self.nombres = nombres
        
    #print(generate_password_hash('123456'))

    def login(self, conexion):
        cursor = conexion.cursor()
        sql = """ SELECT * FROM usuarios WHERE email = '{0}' """.format(self.email)
        cursor.execute(sql)
        fila = cursor.fetchone()
        if fila != None:
            usuario = Usuario(fila[0], fila[1], check_password_hash(fila[2],self.password),fila[3])
            return usuario
            
        else:
            return None
        
    @classmethod
    def obtener_usuario(self, conexion, id):
        cursor = conexion.cursor()
        sql = """ SELECT id, email, nombres
            FROM usuarios
            WHERE id = {0} """.format(id)
        cursor.execute(sql)
        fila = cursor.fetchone()
        if fila != None:
            usuario = Usuario(fila[0], fila[1], None, fila[2])
            return usuario
        else:
            return None