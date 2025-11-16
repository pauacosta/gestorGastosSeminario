# Importamos las librerías necesarias
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Creamos el objeto de base de datos
db = SQLAlchemy()

# =============================================================
# MODELO DE USUARIO
# =============================================================
class Usuario(db.Model):
    """
    Modelo que representa un usuario del sistema.
    Cada usuario puede tener múltiples gastos.
    """
    __tablename__ = 'usuarios'  # Nombre de la tabla en la base de datos
   
    # Columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)  # ID único del usuario
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nombre de usuario único
    email = db.Column(db.String(120), unique=True, nullable=False)  # Email único
    password_hash = db.Column(db.String(200), nullable=False)  # Contraseña encriptada
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha de creación
   
    # Relación con la tabla Gasto
    # 'gastos' es el nombre que usaremos para acceder a los gastos del usuario
    # backref='usuario' permite acceder al usuario desde un gasto (gasto.usuario)
    # cascade='all, delete-orphan' significa que si eliminamos un usuario,
    # también se eliminan todos sus gastos
    gastos = db.relationship('Gasto', backref='usuario', lazy=True, cascade='all, delete-orphan')
   
    def set_password(self, password):
        """
        Método para guardar la contraseña de forma segura.
        La contraseña se guarda encriptada (hash) en la base de datos.
        """
        self.password_hash = generate_password_hash(password)
   
    def check_password(self, password):
        """
        Método para verificar si una contraseña es correcta.
        Compara la contraseña ingresada con el hash guardado.
        """
        return check_password_hash(self.password_hash, password)
   
    def __repr__(self):
        """
        Representación del objeto cuando lo imprimimos.
        Útil para debugging.
        """
        return f'<Usuario {self.username}>'

# =============================================================
# MODELO DE CATEGORÍA
# =============================================================
class Categoria(db.Model):
    """
    Modelo que representa una categoría de gastos.
    Ejemplos: Comida, Transporte, Entretenimiento, etc.
    """
    __tablename__ = 'categorias'  # Nombre de la tabla
   
    # Columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)  # ID único de la categoría
    nombre = db.Column(db.String(100), unique=True, nullable=False)  # Nombre único
    descripcion = db.Column(db.String(200))  # Descripción opcional
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha de creación
   
    # Relación con la tabla Gasto
    # Una categoría puede tener múltiples gastos
    # backref='categoria' permite acceder a la categoría desde un gasto (gasto.categoria)
    gastos = db.relationship('Gasto', backref='categoria', lazy=True)
   
    def __repr__(self):
        """
        Representación del objeto para debugging.
        """
        return f'<Categoria {self.nombre}>'

# =============================================================
# MODELO DE GASTO
# =============================================================
class Gasto(db.Model):
    """
    Modelo que representa un gasto registrado.
    Cada gasto está asociado a un usuario y a una categoría.
    """
    __tablename__ = 'gastos'  # Nombre de la tabla
   
    # Columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)  # ID único del gasto
    monto = db.Column(db.Float, nullable=False)  # Monto del gasto (obligatorio)
    descripcion = db.Column(db.String(200))  # Descripción del gasto (opcional)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)  # Fecha del gasto
   
    # Claves foráneas (Foreign Keys)
    # Estas columnas conectan el gasto con una categoría y un usuario
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
   
    # Nota: Las relaciones (backref) ya están definidas en Usuario y Categoria
    # Por eso podemos hacer: gasto.usuario y gasto.categoria
   
    def __repr__(self):
        """
        Representación del objeto para debugging.
        """
        return f'<Gasto ${self.monto} - {self.descripcion}>'

# =============================================================
# EXPLICACIÓN DE LAS RELACIONES
# =============================================================
"""
RELACIÓN USUARIO - GASTO (Uno a Muchos):
- Un usuario puede tener muchos gastos
- Un gasto pertenece a un solo usuario
- Si eliminamos un usuario, se eliminan todos sus gastos (cascade)

RELACIÓN CATEGORIA - GASTO (Uno a Muchos):
- Una categoría puede tener muchos gastos
- Un gasto pertenece a una sola categoría
- Si intentamos eliminar una categoría con gastos, debemos validarlo primero

Ejemplo de uso:
    # Obtener todos los gastos de un usuario
    usuario = Usuario.query.get(1)
    gastos = usuario.gastos  # Lista de gastos del usuario
   
    # Obtener la categoría de un gasto
    gasto = Gasto.query.get(1)
    categoria = gasto.categoria  # Objeto Categoria
   
    # Obtener el usuario que hizo un gasto
    usuario = gasto.usuario  # Objeto Usuario
"""