from flask import Flask, render_template, request, redirect, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Category, Record

app = Flask(__name__)
app.secret_key = "super-secret-key"  # cambia esto en producción

# Configuración de base de datos SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt = Bcrypt(app)


# ----------------------------------
# CREAR TABLAS
# ----------------------------------
with app.app_context():
    db.create_all()

    # Crear usuario admin por defecto si no existe ninguno
    if User.query.count() == 0:
        default_email = "admin@admin.com"
        default_password = bcrypt.generate_password_hash("admin").decode("utf-8")

        admin_user = User(email=default_email, password=default_password)
        db.session.add(admin_user)
        db.session.commit()

        print("Usuario inicial creado: admin@admin.com / admin")
def is_logged():
    return "user" in session


# ----------------------------------
# LOGIN
# ----------------------------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        pwd = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, pwd):
            session["user"] = user.email
            return redirect("/form")
        else:
            return render_template("login.html", error="Credenciales incorrectas")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ----------------------------------
# ABM USUARIOS
# ----------------------------------
@app.route("/users", methods=["GET", "POST"])
def users():
    if not is_logged():
        return redirect("/")

    if request.method == "POST":
        email = request.form["email"]
        password = bcrypt.generate_password_hash(
            request.form["password"]
        ).decode("utf-8")

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect("/users")

    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/users/delete/<int:id>")
def delete_user(id):
    if not is_logged():
        return redirect("/")

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


# ----------------------------------
# CATEGORÍAS
# ----------------------------------
@app.route("/categories", methods=["GET", "POST"])
def categories():
    if not is_logged():
        return redirect("/")

    if request.method == "POST":
        name = request.form["name"]
        if not name.strip():
            cats = Category.query.all()
            return render_template(
                "categories.html", categories=cats, error="El nombre es obligatorio"
            )
        db.session.add(Category(name=name.strip()))
        db.session.commit()
        return redirect("/categories")

    categories = Category.query.all()
    return render_template("categories.html", categories=categories)


@app.route("/categories/delete/<int:id>")
def delete_category(id):
    if not is_logged():
        return redirect("/")

    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()

    return redirect("/categories")


# ----------------------------------
# FORMULARIO DE CARGA
# ----------------------------------
@app.route("/form", methods=["GET", "POST"])
def form():
    if not is_logged():
        return redirect("/")

    categories = Category.query.all()

    if request.method == "POST":
        category_id = request.form["category"]
        amount = request.form["amount"]
        description = request.form["description"]

        try:
            amount_value = float(amount)
        except ValueError:
            return render_template(
                "form.html",
                categories=categories,
                error="El monto debe ser numérico",
            )

        record = Record(
            category_id=category_id, amount=amount_value, description=description
        )
        db.session.add(record)
        db.session.commit()

        return redirect("/list")

    return render_template("form.html", categories=categories)


# ----------------------------------
# LISTADO
# ----------------------------------
@app.route("/list")
def list_data():
    if not is_logged():
        return redirect("/")

    records = Record.query.all()
    return render_template("list.html", records=records)


# ----------------------------------
# PÁGINA SIMPLE DE INICIO / MENU
# ----------------------------------
@app.route("/home")
def home():
    if not is_logged():
        return redirect("/")
    return render_template("home.html")


# ----------------------------------
# RUN
# ----------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
