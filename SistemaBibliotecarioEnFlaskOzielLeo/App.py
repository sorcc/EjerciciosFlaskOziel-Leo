from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#Conectar a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'biblitecaleoyoziel'
mysql = MySQL(app)

#configuraciones
app.secret_key = 'mysecretkey'

@app.route("/")
def inicio():
    return render_template("contraseña.html")

@app.route('/Login', methods=['POST'])
def login():
    if request.method == 'POST':
        usuario=request.form['usuario']
        password=request.form['password']
        # Validación básica de ejemplo
        if usuario == 'admin' and password == '1234':
            return render_template("menu.html")
        else:
            flash('Contraseña incorrecta, vuelve a intentarlo')
            return render_template("contraseña.html")

@app.route("/Menuprincipal")
def Menuprincipal():
    return render_template("menu.html")

@app.route("/Empleados")
def Empleados():
    return render_template("empleados.html")

# Ir a la Pagina de inicio
@app.route('/Libros')
def Libros():
    cur = mysql.connection.cursor()
    cur.execute('select * from libros')
    data = cur.fetchall()
    print(data)
    #return "Bienvenido al sistema Bibliotecario 1.0"
    return render_template('libros.html', libros = data)

@app.route('/Agregar_Libro', methods=['POST'])
def Agregar_Libro():
    #return 'Modulo: Agregar Libro'

    if request.method == 'POST':
        id=request.form['id']
        titulo=request.form['titulo']
        autor=request.form['autor']
        edicion=request.form['edicion']
        año=request.form['año']
        editorial=request.form['editorial']
        nopaginas=request.form['nopaginas']
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO libros (Titulo,Autor,Edicion,Año,Editorial,NoPaginas) VALUES (%s,%s,%s,%s,%s,%s)',
                    (titulo,autor,edicion,año,editorial,nopaginas))
        mysql.connection.commit()
        flash('Libro Agregado satisfactoriamente')
        return redirect(url_for('Libros'))

@app.route('/ModificarLibro/<id>')
def ModificarLibro(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM libros where id=%s', (id,))
    data = cur.fetchall()
    print(data)
    return render_template('modificarLibros.html', libros = data[0])

@app.route('/ActualizarLibro/<id>', methods=['POST'])
def ActualizarLibro(id):
    if request.method == 'POST':
        #id=request.form['id']
        titulo=request.form['titulo']
        autor=request.form['autor']
        edicion=request.form['edicion']
        año=request.form['año']
        editorial=request.form['editorial']
        nopaginas=request.form['nopaginas']
        cur=mysql.connection.cursor()
        cur.execute("""
            UPDATE libros
            SET Titulo=%s,
                Autor=%s,
                Edicion=%s,
                Año=%s,
                Editorial=%s,
                NoPaginas=%s
            WHERE id=%s
        """, (titulo,autor,edicion,año,editorial,nopaginas,id))
        mysql.connection.commit()
        flash('Libro actualizado exitosamente')
        return redirect(url_for('Libros'))

# ------------------------------USUARIOS------------------------------
@app.route('/Usuarios')
def Usuarios():
    cur = mysql.connection.cursor()
    cur.execute('select * from usuarios')
    data = cur.fetchall()
    return render_template('usuarios.html', usuarios = data)

@app.route('/Agregar_Usuario', methods=['POST'])
def Agregar_Usuario():
    #return 'Modulo: Agregar Usuario'

    if request.method == 'POST':
        id=request.form['id']
        nombre=request.form['nombre']
        direccion=request.form['direccion']
        telefono=request.form['telefono']
        correo=request.form['correo']
        curp=request.form['curp']
        cur=mysql.connection.cursor()
        cur.execute('INSERT INTO usuarios (Nombre,Direccion,Telefono,Correo,curp) VALUES (%s,%s,%s,%s,%s)',
        (nombre,direccion,telefono,correo,curp))
        mysql.connection.commit()
        flash('Usuario Agregado satisfactoriamente')
        return redirect(url_for('Usuarios'))

@app.route('/ModificarUsuario/<id>')
def ModificarUsuario(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuarios where id=%s', (id,))
    data = cur.fetchall()
    print(data)
    return render_template('modificarUsuarios.html', usuarios = data[0])

@app.route('/ActualizarUsuario/<id>', methods=['POST'])
def ActualizarUsuario(id):
    if request.method == 'POST':
        #id=request.form['id']
        nombre=request.form['nombre']
        direccion=request.form['direccion']
        telefono=request.form['telefono']
        correo=request.form['correo']
        curp=request.form['curp']
        cur= mysql.connection.cursor()
        cur.execute("""
            UPDATE usuarios
            SET Nombre=%s,
                Direccion=%s,
                Telefono=%s,
                Correo=%s,
                Curp=%s
            WHERE id=%s
        """, (nombre,direccion,telefono,correo,curp,id))
        mysql.connection.commit()
        flash('Usuario actualizado exitosamente')
        return redirect(url_for('Usuarios'))

@app.route('/EliminarUsuario/<string:id>')
def EliminarUsuario(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from usuarios where id={}'.format(id))
    mysql.connection.commit()
    flash('Usuario eliminado satisfactoriamente')
    return redirect(url_for('Usuarios'))

@app.route('/EliminarLibro/<string:id>')
def EliminarLibro(id):
    cur = mysql.connection.cursor()
    cur.execute('delete from libros where id={}'.format(id))
    mysql.connection.commit()
    flash('Libro eliminado satisfactoriamente')
    return redirect(url_for('Libros'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)