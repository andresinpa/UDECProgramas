from flask import Flask, flash, redirect, render_template, request, url_for
from usuario import Usuario

from config import *
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = "admin"
login_manager = LoginManager(app)
csrf = CSRFProtect()

con_bd = EstablecerConexion()

#----------------- CREACION DE TABLAS -----------------------------------------
def CrearTablaUsuarios():
    cursor = con_bd.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
    id serial NOT NULL,
    email character varying(50),
    password character varying(102),
    nombres character varying(60),
    CONSTRAINT pk_usuarios_id PRIMARY KEY (id)
    );
    """)
    con_bd.commit()
    
def CrearTablaProgramas():
    cursor = con_bd.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS programas(
    id serial NOT NULL,
    nombre character varying(200),
    titulo character varying(200),
    metodologia character varying(200),
    creditos character varying(10),
    duracion character varying(10),
    mision text,
    vision text,
    imagen character varying(200),
    CONSTRAINT pk_programas_id PRIMARY KEY (id)
    );
    """)
    con_bd.commit()

#--------------------PAGINA PRINCIPAL Y LOGIN DE ADMIN -----------------------------------------------------    
@app.route('/')  # decorator to register a route with the app
def index():
    return render_template('index.html')


@app.route('/admin', methods=['GET','POST'])
def inicio():
    if request.method == 'POST':
        user = Usuario(0, request.form['email'], request.form['password'])
        usuario_logueado = Usuario.login(user,con_bd)
        if usuario_logueado != None:
            if usuario_logueado.password:
                login_user(usuario_logueado)
                return redirect(url_for('administracion'))
            else:
                flash("Contraseña Incorrecta","error")
                return render_template('index.html')
        else:
            flash("No existe el usuario","error")
            return render_template('index.html')
    else:
        return render_template('index.html')

@login_manager.user_loader
def cargar_usuario(id):
    return Usuario.obtener_usuario(con_bd,id)

@app.route('/cerrar_sesion')
def cerrar_sesion():
    logout_user()
    return render_template('index.html')

#-----------------ADMINISTRACION DE PROGRAMAS ---------------------------

@app.route('/administracion')
@login_required
def administracion():
    cursor = con_bd.cursor()
    sql = "SELECT*FROM programas"
    cursor.execute(sql)
    ProgramasRegistrados = cursor.fetchall()
    return render_template('administracion.html', programas = ProgramasRegistrados)

@app.route('/guardar_programas', methods = ['POST'])
def agregarPrograma():
    
    cursor = con_bd.cursor()
    nombre = request.form['nombre']
    titulo = request.form['titulo']
    metodologia = request.form['metodologia']
    creditos = request.form['creditos']
    duracion = request.form['duracion']
    mision = request.form['mision']
    vision = request.form['vision']
    imagen = request.form['imagen']
    
    
    if nombre and titulo and metodologia and creditos and duracion and mision and  vision and imagen:
        sql = """INSERT INTO programas(nombre, titulo, metodologia, creditos, duracion, mision, vision, imagen) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    
        cursor.execute(sql,(nombre, titulo, metodologia, creditos, duracion, mision, vision, imagen))
        
        con_bd.commit()
        flash("Registro guardado correctamente", "info")
        return redirect(url_for('administracion'))
    else:
        return "Error en la consulta"


@app.route('/eliminar_programa/<int:id>', methods=['POST'])
def eliminar(id):
    if request.method == 'POST':
        cursor = con_bd.cursor()
        sql = """DELETE FROM programas WHERE id = %s"""
        cursor.execute(sql, (id,))
        con_bd.commit()
        flash("Programa eliminado correctamente", "info")
        return redirect(url_for('administracion'))
    return render_template('administracion.html')

#--------- VISTAS DE PROGRAMAS ---------------------------------------------------------------
@app.route('/general')
def general():
    cursor = con_bd.cursor()
    sql = "SELECT*FROM programas"
    cursor.execute(sql)
    ProgramasRegistrados = cursor.fetchall()
    return render_template('programas.html', programas = ProgramasRegistrados)

@app.route('/individual/<int:programa_id>')
def vista_individual(programa_id):
    cursor = con_bd.cursor()
    sql = "SELECT * FROM programas WHERE id = %s"
    cursor.execute(sql, (programa_id,))
    programa_individual = cursor.fetchone()
    return render_template('vistaIndividual.html', programa=programa_individual)



#-------------- MANEJO DE ERRORES ---------------------------------------------------
def error_401(error):
    return render_template('index.html')
def error_404(error):
    return "Página NO Encontrada", 404


#--------------------- INICIALIZACION ------------------------------------
if __name__ == '__main__':
    csrf.init_app(app)
    app.register_error_handler(401, error_401)
    app.register_error_handler(404, error_404)
    CrearTablaUsuarios()
    CrearTablaProgramas()
    app.run(debug=True)