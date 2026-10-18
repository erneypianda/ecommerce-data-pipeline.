"""Comprueba la primera conexión de Python a PostgreSQL."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


def load_database_url() -> str:
    """Lee .env y arma la URL de conexión sin imprimir secretos."""
    project_root = Path(__file__).resolve().parents[1]
    env_path = project_root / ".env"

    if not env_path.exists():
        raise FileNotFoundError(
            f"No existe {env_path}. Copia .env.example a .env y completa DB_PASSWORD."
        )

    load_dotenv(env_path)

    required = ("DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD")
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise ValueError(
            "Faltan variables en .env: "
            + ", ".join(missing)
            + ". Edita .env en la carpeta del proyecto y guarda el archivo."
        )

    host = os.environ["DB_HOST"]
    port = os.environ["DB_PORT"]
    name = os.environ["DB_NAME"]
    user = os.environ["DB_USER"]
    password = quote_plus(os.environ["DB_PASSWORD"])

    # postgresql+psycopg usa el driver psycopg 3 con SQLAlchemy.
    return f"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}"


def main() -> int:
    try:
        database_url = load_database_url()
        engine = create_engine(database_url)

        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            database_name = connection.execute(
                text("SELECT current_database()")
            ).scalar_one()

        print(f"Conexion correcta. Base de datos activa: {database_name}")
        return 0

    except (FileNotFoundError, ValueError) as exc:
        print(f"Error de configuracion: {exc}", file=sys.stderr)
        return 1
    except SQLAlchemyError as exc:
        # No imprimimos la URL ni la contraseña; solo el tipo de fallo.
        print(
            "Error al conectar con PostgreSQL. "
            "Revisa host, puerto, nombre de base, usuario y contraseña en .env. "
            f"Detalle tecnico: {exc.__class__.__name__}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
