"""
Explora el archivo de productos de Olist.
Solo lee e imprime informacion. No modifica el CSV.
"""

import os
import pandas as pd

# Ruta del proyecto y del CSV de productos
PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRODUCTS_FILE = os.path.join(
    PROJECT_FOLDER,
    "data",
    "raw",
    "olist",
    "olist_products_dataset.csv",
)

# Columnas de peso y medidas
SIZE_COLUMNS = [
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
]


def main():
    # 1) Comprobar que el archivo existe
    if not os.path.exists(PRODUCTS_FILE):
        print("No se encontro el archivo:", PRODUCTS_FILE)
        return

    # 2) Leer el CSV
    df = pd.read_csv(PRODUCTS_FILE)

    print("=" * 60)
    print("Explorando productos de Olist")
    print("=" * 60)

    # 3) Cuantos productos hay (una fila = un producto)
    total_products = len(df)
    print("1) Cantidad de productos:", total_products)

    # 4) Productos con al menos un valor nulo en cualquier columna
    #    axis=1 revisa fila por fila
    rows_with_nulls = df.isna().any(axis=1)
    products_with_nulls = rows_with_nulls.sum()
    print("2) Productos con algun valor nulo:", int(products_with_nulls))

    # 5) Productos sin categoria
    empty_category = df["product_category_name"].isna().sum()
    print("3) Productos con product_category_name vacio:", int(empty_category))

    # 6) Productos con peso o alguna dimension nula
    has_size_null = df[SIZE_COLUMNS].isna().any(axis=1)
    products_with_size_nulls = has_size_null.sum()
    print("4) Productos con peso o dimensiones nulos:", int(products_with_size_nulls))

    # 7) Cinco ejemplos de productos con datos faltantes
    print("5) Cinco ejemplos de productos con datos faltantes:")
    missing_rows = df[rows_with_nulls]

    if len(missing_rows) == 0:
        print("  No hay productos con datos faltantes.")
    else:
        # Tomamos solo las primeras 5 filas con nulos
        examples = missing_rows.head(5)

        for index, row in examples.iterrows():
            product_id = row["product_id"]

            # Buscamos que columnas estan vacias en esta fila
            missing_columns = []
            for column in df.columns:
                if pd.isna(row[column]):
                    missing_columns.append(column)

            print(f"  - product_id: {product_id}")
            print(f"    columnas afectadas: {missing_columns}")

    # 8) Revisar si hay product_id repetidos
    duplicated_ids = df["product_id"].duplicated().sum()
    print("6) product_id duplicados:", int(duplicated_ids))

    if duplicated_ids == 0:
        print("   Cada product_id aparece una sola vez.")
    else:
        print("   Cuidado: hay product_id repetidos.")

    print("=" * 60)
    print("Exploracion terminada. El CSV original no se modifico.")


if __name__ == "__main__":
    main()
