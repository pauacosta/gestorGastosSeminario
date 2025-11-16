# 💰 Gestor de Gastos - Versión Mejorada

Sistema completo de gestión de gastos con interfaz moderna y todas las funcionalidades ABM.

## ✨ Características Nuevas

### 🎨 UI Moderna y Atractiva
- Diseño moderno con gradientes y animaciones
- Interfaz responsive (funciona en móviles, tablets y desktop)
- Colores vibrantes y profesionales
- Iconos Font Awesome para mejor experiencia visual
- Efectos hover y transiciones suaves

### 📋 ABM Completo de Categorías
- ✅ Crear nuevas categorías con descripción
- ✅ Editar categorías existentes
- ✅ Eliminar categorías (con validación de gastos asociados)
- ✅ Ver cantidad de gastos por categoría

### 👥 ABM Completo de Usuarios
- ✅ Crear nuevos usuarios con email y contraseña
- ✅ Editar información de usuarios
- ✅ Cambiar contraseñas
- ✅ Eliminar usuarios (excepto el usuario logueado)
- ✅ Ver cantidad de gastos por usuario

### ⚠️ Validaciones Mejoradas
- ✅ **Validación obligatoria de categoría**: No se puede crear un gasto sin seleccionar categoría
- ✅ Mensajes de error claros y visibles
- ✅ Validación de montos positivos
- ✅ Validación de usuarios y emails duplicados
- ✅ Alertas en tiempo real con JavaScript

### 📊 Dashboard Mejorado
- Estadísticas visuales con tarjetas de información
- Total de gastos, categorías y suma total
- Acciones rápidas
- Información del sistema

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/pauacosta/gestorGastosSeminario.git
cd gestorGastosSeminario
```

### 2. Crear entorno virtual
```bash
python -m venv .venv

# En Windows:
.venv\Scripts\activate

# En Linux/Mac:
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación
```bash
python app.py
```

### 5. Abrir en el navegador
```
http://localhost:5000
```

## 🔐 Credenciales por Defecto

```
Usuario: admin
Contraseña: admin123
```

## 📁 Estructura del Proyecto

```
gestorGastosSeminario/
├── app.py                    # Aplicación Flask principal
├── models.py                 # Modelos de base de datos
├── requirements.txt          # Dependencias
├── database.db              # Base de datos SQLite (se crea automáticamente)
├── templates/
│   ├── base.html           # Template base con navbar y estilos
│   ├── login.html          # Página de login
│   ├── home.html           # Dashboard principal
│   ├── usuarios.html       # ABM de usuarios
│   ├── categorias.html     # ABM de categorías
│   ├── form.html           # Formulario de gastos
│   └── list.html           # Lista de gastos
└── README.md
```

## 🎯 Funcionalidades Principales

### 1. Gestión de Usuarios
- Ver lista completa de usuarios
- Crear nuevos usuarios con validación
- Editar usuarios existentes
- Eliminar usuarios (con protección del usuario actual)
- Ver estadísticas de gastos por usuario

### 2. Gestión de Categorías
- Ver todas las categorías con descripciones
- Crear categorías con nombre único
- Editar categorías existentes
- Eliminar categorías vacías
- Validación de categorías con gastos asociados

### 3. Gestión de Gastos
- **Validación obligatoria de categoría**
- Formulario intuitivo con ayudas visuales
- Lista completa con detalles
- Modal de detalles expandido
- Filtrado por fecha (más recientes primero)
- Suma total automática

### 4. Dashboard
- Estadísticas visuales
- Accesos rápidos
- Información del sistema
- Consejos útiles

## 🔒 Seguridad

- Contraseñas hasheadas con Werkzeug
- Sesiones seguras con Flask
- Validación en frontend y backend
- Protección contra usuarios duplicados
- Control de permisos (no se puede eliminar el usuario logueado)

## 💡 Mejoras Implementadas

### UI/UX
- ✅ Gradientes modernos en toda la interfaz
- ✅ Animaciones suaves al cargar elementos
- ✅ Cards con efecto hover
- ✅ Badges y etiquetas coloridas
- ✅ Modals centrados y estilizados
- ✅ Formularios con iconos y ayudas visuales
- ✅ Responsive design completo

### Funcionalidad
- ✅ Validación de categoría obligatoria con mensaje de error
- ✅ ABM completo de usuarios
- ✅ ABM completo de categorías
- ✅ Validaciones robustas en todos los formularios
- ✅ Mensajes flash informativos
- ✅ Confirmaciones antes de eliminar
- ✅ Modals para crear/editar sin cambiar de página

### Base de Datos
- ✅ Relaciones entre tablas correctas
- ✅ Cascade delete para gastos de usuarios
- ✅ Validación de integridad referencial
- ✅ Timestamps automáticos

## 📝 Notas Importantes

1. **Categoría Obligatoria**: El sistema no permite crear gastos sin categoría. Si no hay categorías, el botón de guardar estará deshabilitado.

2. **Usuarios**: No puedes eliminar tu propio usuario mientras estés logueado.

3. **Categorías**: No puedes eliminar categorías que tengan gastos asociados.

4. **Base de Datos**: Se crea automáticamente al ejecutar la aplicación por primera vez.

## 🎨 Paleta de Colores

- **Primary**: #6366f1 (Índigo)
- **Secondary**: #8b5cf6 (Púrpura)
- **Success**: #10b981 (Verde)
- **Danger**: #ef4444 (Rojo)
- **Warning**: #f59e0b (Ámbar)

## 🤝 Contribuir

Este proyecto es de código abierto. Siéntete libre de hacer fork y contribuir.

## 📄 Licencia

MIT License

---

**Desarrollado con ❤️ usando Flask, Bootstrap 5 y Font Awesome**
