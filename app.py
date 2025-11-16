# Importamos las librerías necesarias
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from models import db, Usuario, Categoria, Gasto
from datetime import datetime

# Creamos la aplicación Flask
app = Flask(__name__)

# Configuraciones de la aplicación
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'  # Clave secreta para las sesiones
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Ubicación de la base de datos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar mensajes de modificación

# Inicializamos la base de datos con la aplicación
db.init_app(app)

# Crear las tablas si no existen
with app.app_context():
    db.create_all()
    # Crear usuario admin por defecto si no existe
    usuario_admin = Usuario.query.filter_by(username='admin').first()
    if not usuario_admin:
        admin = Usuario(username='admin', email='admin@example.com')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

# =============================================================
# DECORADOR PARA PROTEGER RUTAS (requiere estar logueado)
# =============================================================
def login_required(f):
    """
    Este decorador verifica si el usuario está logueado.
    Si no está logueado, lo redirige al login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificamos si existe 'user_id' en la sesión
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# =============================================================
# RUTA PRINCIPAL
# =============================================================
@app.route('/')
def index():
    """
    Página de inicio.
    Si el usuario está logueado, va al home.
    Si no, va al login.
    """
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

# =============================================================
# RUTAS DE AUTENTICACIÓN (LOGIN Y LOGOUT)
# =============================================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Página de login.
    GET: Muestra el formulario de login
    POST: Procesa el login del usuario
    """
    if request.method == 'POST':
        # Obtenemos los datos del formulario
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Buscamos el usuario en la base de datos
        usuario = Usuario.query.filter_by(username=username).first()
        
        # Verificamos si el usuario existe y la contraseña es correcta
        if usuario and usuario.check_password(password):
            # Guardamos la información en la sesión
            session['user_id'] = usuario.id
            session['username'] = usuario.username
            flash(f'¡Bienvenido {username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    # Si es GET o el login falló, mostramos el formulario
    return render_template('login.html')

@app.route('/logout')
def logout():
    """
    Cerrar sesión del usuario.
    Limpia toda la información de la sesión.
    """
    session.clear()
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('login'))

# =============================================================
# RUTA HOME (DASHBOARD)
# =============================================================
@app.route('/home')
@login_required
def home():
    """
    Página principal (Dashboard).
    Muestra estadísticas generales del sistema.
    """
    # Contamos la cantidad de gastos
    total_gastos = Gasto.query.count()
    
    # Contamos la cantidad de categorías
    total_categorias = Categoria.query.count()
    
    # Calculamos la suma total de todos los gastos
    suma_total = db.session.query(db.func.sum(Gasto.monto)).scalar() or 0
    
    # Renderizamos la página pasando las estadísticas
    return render_template('home.html', 
                         total_gastos=total_gastos,
                         total_categorias=total_categorias,
                         suma_total=suma_total)

# =============================================================
# RUTAS DE USUARIOS (ABM - Alta, Baja, Modificación)
# =============================================================
@app.route('/usuarios')
@login_required
def usuarios():
    """
    Muestra la lista de todos los usuarios.
    """
    # Obtenemos todos los usuarios de la base de datos
    usuarios = Usuario.query.all()
    return render_template('usuarios.html', usuarios=usuarios)

@app.route('/usuarios/crear', methods=['POST'])
@login_required
def crear_usuario():
    """
    Crea un nuevo usuario.
    Recibe: username, email, password
    """
    # Obtenemos los datos del formulario
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Verificamos si el username ya existe
    if Usuario.query.filter_by(username=username).first():
        flash('El nombre de usuario ya existe', 'danger')
        return redirect(url_for('usuarios'))
    
    # Verificamos si el email ya existe
    if Usuario.query.filter_by(email=email).first():
        flash('El email ya está registrado', 'danger')
        return redirect(url_for('usuarios'))
    
    # Creamos el nuevo usuario
    nuevo_usuario = Usuario(username=username, email=email)
    nuevo_usuario.set_password(password)  # La contraseña se guarda encriptada
    
    # Guardamos en la base de datos
    db.session.add(nuevo_usuario)
    db.session.commit()
    
    flash(f'Usuario {username} creado exitosamente', 'success')
    return redirect(url_for('usuarios'))

@app.route('/usuarios/editar/<int:id>', methods=['POST'])
@login_required
def editar_usuario(id):
    """
    Edita un usuario existente.
    Recibe el ID del usuario por la URL.
    """
    # Buscamos el usuario en la base de datos
    usuario = Usuario.query.get_or_404(id)
    
    # Obtenemos los nuevos datos del formulario
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    
    # Verificamos si el username ya existe en otro usuario
    usuario_existente = Usuario.query.filter_by(username=username).first()
    if usuario_existente and usuario_existente.id != id:
        flash('El nombre de usuario ya existe', 'danger')
        return redirect(url_for('usuarios'))
    
    # Verificamos si el email ya existe en otro usuario
    email_existente = Usuario.query.filter_by(email=email).first()
    if email_existente and email_existente.id != id:
        flash('El email ya está registrado', 'danger')
        return redirect(url_for('usuarios'))
    
    # Actualizamos los datos del usuario
    usuario.username = username
    usuario.email = email
    
    # Solo actualizamos la contraseña si se proporcionó una nueva
    if password:
        usuario.set_password(password)
    
    # Guardamos los cambios
    db.session.commit()
    flash(f'Usuario {username} actualizado exitosamente', 'success')
    return redirect(url_for('usuarios'))

@app.route('/usuarios/eliminar/<int:id>')
@login_required
def eliminar_usuario(id):
    """
    Elimina un usuario de la base de datos.
    No permite eliminar el usuario que está logueado.
    """
    # Buscamos el usuario
    usuario = Usuario.query.get_or_404(id)
    
    # Verificamos que no sea el usuario actual
    if usuario.id == session['user_id']:
        flash('No puedes eliminar tu propio usuario', 'danger')
        return redirect(url_for('usuarios'))
    
    # Eliminamos el usuario
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado exitosamente', 'success')
    return redirect(url_for('usuarios'))

# =============================================================
# RUTAS DE CATEGORÍAS (ABM - Alta, Baja, Modificación)
# =============================================================
@app.route('/categorias')
@login_required
def categorias():
    """
    Muestra la lista de todas las categorías.
    """
    # Obtenemos todas las categorías de la base de datos
    categorias = Categoria.query.all()
    return render_template('categorias.html', categorias=categorias)

@app.route('/categorias/crear', methods=['POST'])
@login_required
def crear_categoria():
    """
    Crea una nueva categoría.
    Recibe: nombre, descripción
    """
    # Obtenemos los datos del formulario
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion', '')  # La descripción es opcional
    
    # Verificamos si la categoría ya existe
    if Categoria.query.filter_by(nombre=nombre).first():
        flash('La categoría ya existe', 'danger')
        return redirect(url_for('categorias'))
    
    # Creamos la nueva categoría
    nueva_categoria = Categoria(nombre=nombre, descripcion=descripcion)
    
    # Guardamos en la base de datos
    db.session.add(nueva_categoria)
    db.session.commit()
    
    flash(f'Categoría "{nombre}" creada exitosamente', 'success')
    return redirect(url_for('categorias'))

@app.route('/categorias/editar/<int:id>', methods=['POST'])
@login_required
def editar_categoria(id):
    """
    Edita una categoría existente.
    Recibe el ID de la categoría por la URL.
    """
    # Buscamos la categoría en la base de datos
    categoria = Categoria.query.get_or_404(id)
    
    # Obtenemos los nuevos datos del formulario
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion', '')
    
    # Verificamos si el nombre ya existe en otra categoría
    categoria_existente = Categoria.query.filter_by(nombre=nombre).first()
    if categoria_existente and categoria_existente.id != id:
        flash('Ya existe una categoría con ese nombre', 'danger')
        return redirect(url_for('categorias'))
    
    # Actualizamos los datos de la categoría
    categoria.nombre = nombre
    categoria.descripcion = descripcion
    
    # Guardamos los cambios
    db.session.commit()
    flash(f'Categoría "{nombre}" actualizada exitosamente', 'success')
    return redirect(url_for('categorias'))

@app.route('/categorias/eliminar/<int:id>')
@login_required
def eliminar_categoria(id):
    """
    Elimina una categoría de la base de datos.
    No permite eliminar si tiene gastos asociados.
    """
    # Buscamos la categoría
    categoria = Categoria.query.get_or_404(id)
    
    # Verificamos si tiene gastos asociados
    if categoria.gastos:
        flash('No se puede eliminar la categoría porque tiene gastos asociados', 'danger')
        return redirect(url_for('categorias'))
    
    # Eliminamos la categoría
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoría eliminada exitosamente', 'success')
    return redirect(url_for('categorias'))

# =============================================================
# RUTAS DE GASTOS
# =============================================================
@app.route('/gastos')
@login_required
def gastos():
    """
    Muestra el formulario para crear un nuevo gasto.
    """
    # Obtenemos todas las categorías para mostrar en el select
    categorias = Categoria.query.all()
    return render_template('form.html', categorias=categorias)

@app.route('/gastos/crear', methods=['POST'])
@login_required
def crear_gasto():
    """
    Crea un nuevo gasto.
    Recibe: categoria_id, monto, descripción
    VALIDACIÓN IMPORTANTE: La categoría es obligatoria.
    """
    # Obtenemos los datos del formulario
    categoria_id = request.form.get('categoria_id')
    monto = request.form.get('monto')
    descripcion = request.form.get('descripcion', '')
    
    # VALIDACIÓN: Verificamos que se haya seleccionado una categoría
    if not categoria_id:
        flash('Debes seleccionar una categoría', 'danger')
        return redirect(url_for('gastos'))
    
    # VALIDACIÓN: Verificamos que el monto sea válido
    try:
        monto = float(monto)
        if monto <= 0:
            raise ValueError  # El monto debe ser positivo
    except (ValueError, TypeError):
        flash('El monto debe ser un número positivo', 'danger')
        return redirect(url_for('gastos'))
    
    # Creamos el nuevo gasto
    nuevo_gasto = Gasto(
        categoria_id=categoria_id,
        monto=monto,
        descripcion=descripcion,
        usuario_id=session['user_id']  # Asociamos el gasto al usuario logueado
    )
    
    # Guardamos en la base de datos
    db.session.add(nuevo_gasto)
    db.session.commit()
    
    flash('Gasto registrado exitosamente', 'success')
    return redirect(url_for('lista_gastos'))

@app.route('/gastos/lista')
@login_required
def lista_gastos():
    """
    Muestra la lista de todos los gastos.
    Los gastos se ordenan por fecha (más recientes primero).
    """
    # Obtenemos todos los gastos ordenados por fecha descendente
    gastos = Gasto.query.order_by(Gasto.fecha.desc()).all()
    
    # Calculamos el total de todos los gastos
    total = db.session.query(db.func.sum(Gasto.monto)).scalar() or 0
    
    return render_template('list.html', gastos=gastos, total=total)

@app.route('/gastos/eliminar/<int:id>')
@login_required
def eliminar_gasto(id):
    """
    Elimina un gasto de la base de datos.
    """
    # Buscamos el gasto
    gasto = Gasto.query.get_or_404(id)
    
    # Eliminamos el gasto
    db.session.delete(gasto)
    db.session.commit()
    
    flash('Gasto eliminado exitosamente', 'success')
    return redirect(url_for('lista_gastos'))

# =============================================================
# EJECUTAR LA APLICACIÓN
# =============================================================
if __name__ == '__main__':
    # Ejecutamos la aplicación en modo debug
    # host='0.0.0.0' permite acceder desde otras computadoras en la red
    # port=5000 es el puerto donde corre la aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)
