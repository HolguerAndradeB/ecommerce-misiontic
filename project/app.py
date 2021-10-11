from flask import Flask, render_template, url_for

# NOMBRE DE LA APP
app = Flask(__name__)

# :::::::::: ROUTES ::::::::::::

# INDEX
@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')

# LOGIN AND REGISTER
@app.route("/login")
def login():
    return render_template('login.html')

# PRINCIPAL
@app.route("/principal")
def principal():
    return render_template('principal.html')

# LIST-USERS
@app.route("/users")
def users():
    return render_template('users.html')

# EDIT-USER
@app.route("/edit-user")
def get_user():
    return render_template('edit-user.html')

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
    app.run(debug=True, port=3050, host="0.0.0.0")