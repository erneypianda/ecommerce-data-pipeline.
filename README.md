# ecommerce-data-pipeline

Pipeline ETL en Python para cargar datos de ecommerce en PostgreSQL.

El proyecto está en fase de preparación del entorno: Python, dependencias, estructura de carpetas, protección de secretos y conexión a la base de datos. El flujo de extracción, transformación y carga aún no está implementado.

## Objetivo

Construir un pipeline reproducible que:

1. Lea datos de origen (por ejemplo, archivos CSV).
2. Los limpie y transforme con pandas.
3. Los cargue en PostgreSQL usando SQLAlchemy y psycopg.
4. Deje trazabilidad en logs y código versionado.

## Tecnologías

| Componente | Versión / detalle |
|---|---|
| Sistema | Windows 11 |
| Python | 3.15.0 (entorno virtual `.venv`) |
| PostgreSQL | 18 (`ecommerce_db`, puerto 5432) |
| pandas | lectura y transformación de datos |
| SQLAlchemy | acceso a la base de datos |
| psycopg | driver de PostgreSQL |
| python-dotenv | variables de entorno locales |

## Estructura del proyecto

```text
ecommerce-data-pipeline/
├── data/
│   ├── raw/           # datos de origen sin modificar
│   └── processed/     # datos después de transformar
├── logs/              # registros de ejecución
├── src/               # código del proyecto
│   └── test_connection.py
├── tests/             # pruebas automatizadas
├── .env.example       # plantilla de variables (sin secretos)
├── .gitignore
├── requirements.txt
└── README.md
```

Los archivos `.env` y `.venv/` son locales y no deben subirse a Git.

## Configuración del entorno

### 1. Clonar o abrir el proyecto

Abre la carpeta `ecommerce-data-pipeline` en Cursor o en una terminal.

### 2. Crear el entorno virtual

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Comprueba que el intérprete es el del proyecto:

```powershell
python -c "import sys; print(sys.executable)"
```

Debe apuntar a `...\ecommerce-data-pipeline\.venv\Scripts\python.exe`.

### 3. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

### 4. Configurar PostgreSQL

1. Asegúrate de que el servicio `postgresql-x64-18` esté en ejecución.
2. Crea la base de datos `ecommerce_db` en pgAdmin 4 si aún no existe.
3. Copia la plantilla de variables:

```powershell
Copy-Item .env.example .env
```

4. Edita `.env` y completa `DB_PASSWORD` con tu contraseña local. No compartas ese valor ni lo pegues en el chat.

Variables esperadas:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=
```

### 5. Probar la conexión

Con el entorno virtual activo:

```powershell
python src\test_connection.py
```

Si todo está bien, verás un mensaje como:

```text
Conexion correcta. Base de datos activa: ecommerce_db
```

## Seguridad

- `.env` contiene credenciales y está listado en `.gitignore`.
- `.env.example` se puede versionar porque no incluye contraseñas reales.
- El script de conexión no imprime la URL completa ni la contraseña.

## Estado actual

Completado:

- Entorno virtual y dependencias.
- Estructura de carpetas.
- Protección de archivos sensibles.
- Base de datos `ecommerce_db`.
- Prueba de conexión Python → PostgreSQL.

Pendiente:

- Inicializar un repositorio Git propio del proyecto (autorización pendiente).
- Crear tablas del modelo de ecommerce.
- Implementar el pipeline ETL (extract, transform, load).
- Añadir pruebas en `tests/`.
- Publicar el proyecto en un remoto, si se decide más adelante.
