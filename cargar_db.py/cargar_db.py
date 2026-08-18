"""
Carga los CSV del proyecto de retención de alumnos a una base de datos SQLite local.

Uso:
    1. Coloca este script en la raíz de tu repo local (mismo nivel que la carpeta /data)
    2. Corre: python3 cargar_db.py
    3. Se creará el archivo 'taekwondo.db' listo para consultar con SQL
"""

import sqlite3
import csv
import os

DB_NAME = "taekwondo.db"
DATA_DIR = "data"  # carpeta donde están los 6 CSV

TABLAS = {
    "alumnos": {
        "columnas": ["id_alumno", "categoria_edad", "colegio", "id_grupo",
                     "fecha_inscripcion", "estado", "fecha_baja", "motivo_baja"],
        "pk": "id_alumno",
    },
    "grupos": {
        "columnas": ["id_grupo", "colegio", "dia_horario", "instructor", "capacidad_maxima"],
        "pk": "id_grupo",
    },
    "asistencia": {
        "columnas": ["id_asistencia", "id_alumno", "id_grupo", "fecha_clase", "presente"],
        "pk": "id_asistencia",
    },
    "mensualidades": {
        "columnas": ["id_pago", "id_alumno", "mes_pagado", "fecha_pago", "monto", "estatus"],
        "pk": "id_pago",
    },
    "torneos": {
        "columnas": ["id_torneo", "nombre_torneo", "fecha", "sede"],
        "pk": "id_torneo",
    },
    "participacion_torneos": {
        "columnas": ["id_alumno", "id_torneo", "resultado"],
        "pk": None,  # tabla de relación, sin PK propia
    },
}


def crear_tabla(cursor, nombre_tabla, columnas, pk):
    columnas_sql = ", ".join(
        f"{col} TEXT" + (" PRIMARY KEY" if col == pk else "")
        for col in columnas
    )
    cursor.execute(f"DROP TABLE IF EXISTS {nombre_tabla}")
    cursor.execute(f"CREATE TABLE {nombre_tabla} ({columnas_sql})")


def cargar_csv(cursor, nombre_tabla, columnas, ruta_csv):
    with open(ruta_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        filas = [tuple(row[col] for col in columnas) for row in reader]

    placeholders = ", ".join("?" for _ in columnas)
    cursor.executemany(
        f"INSERT INTO {nombre_tabla} VALUES ({placeholders})", filas
    )
    return len(filas)


def main():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    for nombre_tabla, config in TABLAS.items():
        ruta_csv = os.path.join(DATA_DIR, f"{nombre_tabla}.csv")
        if not os.path.exists(ruta_csv):
            print(f"⚠️  No encontré {ruta_csv} — sáltalo o revisa el nombre del archivo")
            continue

        crear_tabla(cursor, nombre_tabla, config["columnas"], config["pk"])
        n_filas = cargar_csv(cursor, nombre_tabla, config["columnas"], ruta_csv)
        print(f"✅ {nombre_tabla}: {n_filas} filas cargadas")

    conn.commit()
    conn.close()
    print(f"\nListo. Base de datos creada: {DB_NAME}")
    print("Ya puedes abrirla con la extensión SQLite de VS Code y correr queries.")


if __name__ == "__main__":
    main()


    