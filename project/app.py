# IMPORTS DE PAQUETES, LIBRERIAS Y MÓDULOS
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import session
from werkzeug.security import generate_password_hash, check_password_hash

import os

dbdir =  "sqlite:///" + os.path.abspath(os.getcwd()) + "/ecommerce.db"

# NOMBRE DE LA APP Y CONFIGURACIONES
app = Flask(__name__)
app.secret_key = 'mysecretkeyholguer'
app.config["SQLALCHEMY_DATABASE_URI"] = dbdir
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# MODELO DE LA BASE DE DATOS A CREAR
class Tercero(db.Model):
    __tablename__ = "Tercero"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.String(100), unique=True, nullable=False)
    identificacion = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    estado = db.Column(db.String(80), nullable=False)
    tipo = db.Column(db.String(80), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class Producto(db.Model):
    __tablename__ = "Producto"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre= db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.Text)

class Comentario(db.Model):
    __tablename__ = "Comentario"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.Text)
    fecha= db.Column(db.String(50))
    idtercero = db.Column(db.Integer, db.ForeignKey('Tercero.id'))
    idproducto = db.Column(db.Integer, db.ForeignKey('Producto.id'))
    
class Calificacion(db.Model):
    __tablename__ = "Calificacion"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    puntaje = db.Column(db.String(5))
    idtercero = db.Column(db.Integer, db.ForeignKey('Tercero.id'))
    idproducto = db.Column(db.Integer, db.ForeignKey('Producto.id'))

class Carrito(db.Model):
    __tablename__ = "Carrito"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Tercero.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('Producto.id'))
    total = db.Column(db.Text,nullable=False)

# ALMACENAMIENTO
# db.create_all()
# producto = Producto.query.all();
tercero = Tercero.query.all();
# box=[]

# :::::::::: ROUTES ::::::::::::
# INDEX
@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')

# LOGIN-AND-REGISTER
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Tercero.query.filter_by(identificacion=request.form["identificacion"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            return redirect(url_for('principal'))
        else:
            flash('Credenciales incorrectas')
            return render_template("login.html")

    return render_template("login.html")

# PRINCIPAL
@app.route("/principal")
def principal():
    return render_template('principal.html')

# LIST-USERS
@app.route("/users")
def users():
    tercero = Tercero.query.all();
    return render_template('users.html', terceros = tercero)

# REGISTER-USERS
@app.route("/add-users", methods=["POST"])
def add_users():
    if request.method == "POST":
        hashed_pw = generate_password_hash(request.form["password"], method="sha256")
        nombres = request.form["nombres"] + " " + request.form["apellidos"]
        identificacion = request.form["identificacion"]
        estado = request.form["estado"]
        tipo = request.form["tipo"]
        telefono = request.form["telefono"]
        email = request.form["email"]
        # OBJETO QUE SE GUARDA EN LA BD
        tercero = Tercero(nombres = nombres, identificacion = identificacion, password=hashed_pw, estado = estado, tipo = tipo, telefono = telefono, email = email)
        db.session.add(tercero)
        db.session.commit()
        flash('Usuario registrado')
        return redirect(url_for('users'))

    return render_template('users.html')
    
# EDIT-USER (CARGAR LA DATA DEL USER)
@app.route("/getuser/<id>")
def getuser(id):
    # tercero = Tercero.query.all();
    tercero = Tercero.query.get(id)
    return render_template('edit-user.html', tercero = tercero)

# EDIT-USER
@app.route('/updateuser/<id>', methods = ['POST'])
def updateuser(id):
    if request.method == 'POST':
        tercero = Tercero.query.filter_by(id=int(id)).first()
        # tercero = session.query(Tercero).filter(Tercero.id == id).first()
        tercero.hashed_pw = generate_password_hash(request.form["password"], method="sha256")
        tercero.nombres = request.form["nombres"]
        tercero.identificacion = request.form["identificacion"]
        tercero.telefono = request.form["telefono"]
        tercero.email = request.form["email"]
        db.session.commit()
        flash('Usuario modificado')
        return redirect(url_for('users'))

    return render_template('./users.html')

# BLOQUEAR-USER
@app.route('/blockuser/<id>')
def blockuser(id):
    tercero = Tercero.query.filter_by(id=int(id)).first()
    if (tercero.estado == 'Inactivo'):
        tercero.estado = 'Activo'
        db.session.commit()
        flash('Usuario desbloqueado')
        return redirect(url_for('users'))
    else:
        tercero.estado = 'Inactivo'
        db.session.commit()
        flash('Usuario bloqueado')
        return redirect(url_for('users'))

# DELETE-USER
@app.route('/deleteuser/<id>')
def deleteuser(id):
    Tercero.query.filter_by(id=int(id)).delete()
    db.session.commit()
    flash('Usuario eliminado')
    return redirect(url_for('users'))

# PROFILE
@app.route("/edit-profile")
def get_profile():
    return render_template('edit-profile.html')

# ADMIN-PRODUCTS
@app.route("/admin-products")
def adminProducts():
    return render_template('admin-products.html')

# EDIT-PRODUCT
@app.route("/edit-product")
def get_product():
    return render_template('edit-product.html')

# MAIN
if __name__ == "__main__":
    db.create_all()
    tercero = Tercero.query.all();
    app.run(debug=True, port=3050, host="0.0.0.0")