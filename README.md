Gestor de Gastos

Proyecto desarrollado como sistema de gestión de gastos personales, con interfaz web y funcionalidades ABM completas.

Características
Interfaz

Interfaz responsive (adaptable a celulares, tablets y computadoras)

Colores definidos y consistentes

Uso de iconos de Font Awesome

Efectos de transición

ABM de Categorías

Crear nuevas categorías con su descripción

Editar categorías existentes

Eliminar categorías (validando si tienen gastos asociados)

Mostrar la cantidad de gastos por categoría

ABM de Usuarios

Crear usuarios con email y contraseña

Editar información de usuarios

Cambiar contraseñas

Eliminar usuarios (excepto el usuario que está logueado)

Ver cantidad de gastos por usuario

Validaciones

Validación obligatoria de categoría (no se puede crear un gasto sin asignarle una)

Mensajes de error claros y visibles

Validación de montos positivos

Control de usuarios y correos duplicados

Alertas en tiempo real con JavaScript

Dashboard

Tarjetas informativas con estadísticas

Totales de gastos, categorías y suma general

Accesos rápidos

Información general del sistema

Instalación
1. Clonar el repositorio
git clone https://github.com/pauacosta/gestorGastosSeminario.git
cd gestorGastosSeminario

2. Crear entorno virtual
python -m venv .venv

# En Windows:
.venv\Scripts\activate

# En Linux/Mac:
source .venv/bin/activate

3. Instalar dependencias
pip install -r requirements.txt

4. Ejecutar la aplicación
python app.py

5. Abrir en el navegador
http://localhost:5000

Credenciales por Defecto
Usuario: admin  
Contraseña: admin123

## Estructura del Proyecto

```
gestorGastosSeminario/
├── app.py                    # Aplicación Flask principal
├── models.py                 # Modelos de base de datos
├── requirements.txt          # Dependencias
├── database.db               # Base de datos SQLite (se genera automáticamente)
├── templates/
│   ├── base.html             # Template base con navbar y estilos
│   ├── login.html            # Página de inicio de sesión
│   ├── home.html             # Dashboard principal
│   ├── usuarios.html         # ABM de usuarios
│   ├── categorias.html       # ABM de categorías
│   ├── form.html             # Formulario de gastos
│   └── list.html             # Lista de gastos
└── README.md
```

Funcionalidades Principales
Gestión de Usuarios

Ver lista completa de usuarios

Crear y editar usuarios

Eliminar usuarios (protegido para el usuario actual)

Ver estadísticas de gastos por usuario

Gestión de Categorías

Listado completo de categorías

Crear, editar y eliminar (solo si no tienen gastos)

Validación de categorías con gastos asociados

Gestión de Gastos

Formulario validado con selección obligatoria de categoría

Listado con detalles y filtrado por fecha

Modal con información ampliada

Cálculo automático del total

Dashboard

Tarjetas informativas con estadísticas

Accesos rápidos a las secciones principales

Información del sistema

Seguridad

Contraseñas encriptadas con Werkzeug

Sesiones seguras con Flask

Validaciones tanto en frontend como en backend

Prevención de duplicados

Control de permisos y restricciones básicas

Mejoras Implementadas
Interfaz y Experiencia de Usuario

Gradientes y animaciones suaves

Tarjetas con efectos hover

Formularios claros con iconos y ayudas visuales

Diseño completamente adaptable

Funcionalidad

ABM de usuarios y categorías completo

Validaciones reforzadas en formularios

Mensajes informativos y de confirmación

Modales para alta y edición sin recargar la página

Base de Datos

Relaciones correctas entre tablas

Eliminación en cascada de gastos de usuarios

Control de integridad referencial

Campos automáticos de fecha y hora

Notas Importantes

No se pueden crear gastos sin una categoría seleccionada.

El usuario actual no puede eliminarse mientras está logueado.

No se pueden eliminar categorías que tengan gastos asociados.

La base de datos se genera automáticamente al ejecutar la aplicación por primera vez.
