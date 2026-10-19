"""
Valida los CSV de Olist.
No modifica los archivos. Solo lee e imprime un resumen.
"""

import os
import pandas as pd

# Carpeta donde estan los CSV (subimos un nivel desde src/ hasta el proyecto)
PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_FOLDER = os.path.join(PROJECT_FOLDER, "data", "raw", "olist")

# Lista de los 9 archivos que esperamos encontrar
FILES = [
    "olist_customers_dataset.csv",
    "olist_geolocation_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_orders_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv",
]


def check_one_file(file_path):
    """Lee un CSV y muestra filas, columnas, nulos y duplicados."""

    # 1) Cargar el archivo en una tabla (DataFrame)
    df = pd.read_csv(file_path)

    # 2) Nombre del archivo (sin la ruta completa)
    file_name = os.path.basename(file_path)

    print("=" * 60)
    print("Archivo:", file_name)
    print("Filas:", len(df))
    print("Columnas:", len(df.columns))
    print("Nombres de columnas:", list(df.columns))

    # 3) Contar nulos en cada columna
    print("Valores nulos por columna:")
    has_nulls = False
    for column in df.columns:
        null_count = df[column].isna().sum()
        if null_count > 0:
            has_nulls = True
            percent = (null_count / len(df)) * 100
            print(f"  - {column}: {null_count} ({percent:.2f}%)")

    if not has_nulls:
        print("  ninguno")

    # 4) Contar filas repetidas completas
    duplicate_count = df.duplicated().sum()
    print("Filas completamente duplicadas:", int(duplicate_count))


def main():
    # Comprobar que existe la carpeta
    if not os.path.isdir(RAW_FOLDER):
        print("No existe la carpeta:", RAW_FOLDER)
        return

    # Comprobar que estan los 9 archivos
    for file_name in FILES:
        file_path = os.path.join(RAW_FOLDER, file_name)
        if not os.path.exists(file_path):
            print("Falta el archivo:", file_name)
            return

    print("Validando", len(FILES), "CSV en:", RAW_FOLDER)

    # Revisar archivo por archivo
    for file_name in FILES:
        file_path = os.path.join(RAW_FOLDER, file_name)
        check_one_file(file_path)

    print("=" * 60)
    print("Validacion terminada. Los CSV originales no se modificaron.")


# Este bloque hace que el script se ejecute al llamarlo desde la terminal
if __name__ == "__main__":
    main()
