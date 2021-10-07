from flask import Flask, render_template, url_for

# NOMBRE DE LA APP
app = Flask(__name__)

# :::::::::: ROUTES ::::::::::::
# INDEX
@app.route("/")
def index():
    return render_template('index.html')

# PRINCIPAL
@app.route("/principal")
def principal():
    return render_template('principal.html')

# USUARIOS
@app.route("/usuarios")
def usuarios():
    return render_template('usuarios.html')

# MAIN
if __name__ == "__main__":
    app.run(debug=True, port=3050, host="0.0.0.0")