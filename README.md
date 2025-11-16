# Gestor simple con Flask + SQLite

Pequeña aplicación web en Python que incluye:

- Sitio de login
- ABM de usuarios
- ABM de categorías
- Formulario de carga de datos con categoría, monto y descripción
- Listado de registros cargados
- Base de datos SQLite (`database.db`)

## 1. Requisitos

- Python 3.9+ instalado

## 2. Cómo ejecutar en tu máquina local

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Luego abrí el navegador en:

- http://127.0.0.1:5000

La base de datos `database.db` se crea automáticamente la primera vez que corrés la app.

## 3. Estructura del proyecto

```text
gestor_gastos_flask_db/
├─ app.py
├─ models.py
├─ requirements.txt
├─ database.db (se generará al correr la app)
├─ templates/
│   ├─ login.html
│   ├─ home.html
│   ├─ users.html
│   ├─ categories.html
│   ├─ form.html
│   └─ list.html
└─ static/
```

## 4. Subir a GitHub

1. Crear un repositorio vacío en GitHub.
2. En esta carpeta:

```bash
git init
git add .
git commit -m "Primer commit - gestor con Flask y SQLite"
git branch -M main
git remote add origin https://github.com/pauacosta/gestorGastosSeminario.git
git push -u origin main
```

## 5. Descargarlo en una VM Linux y correrlo

En la VM:

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip

git clone https://github.com/pauacosta/gestorGastosSeminario.git
cd TU-REPO

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Abrir en la VM (o desde el host, si exponés el puerto):

- http://127.0.0.1:5000
