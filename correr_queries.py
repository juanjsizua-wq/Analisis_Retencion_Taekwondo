"""
Corre automáticamente TODAS las queries .sql que tengas en la carpeta /queries
contra taekwondo.db, y guarda cada resultado como CSV en /resultados.

Así, para agregar una pregunta nueva, solo tienes que:
1. Escribir un nuevo archivo .sql en /queries (ej. query5_algo_nuevo.sql)
2. Correr este script de nuevo — se procesan TODAS las queries automáticamente

Requisitos: pip install pandas --break-system-packages

Uso:
    python3 correr_queries.py
"""

import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "taekwondo.db"


def resolver_directorio(preferido: str, alterno: str) -> Path:
    """Usa el directorio existente y, si no existe ninguno, toma el preferido."""
    dir_preferido = BASE_DIR / preferido
    dir_alterno = BASE_DIR / alterno

    if dir_preferido.exists():
        return dir_preferido
    if dir_alterno.exists():
        return dir_alterno
    return dir_preferido


QUERIES_DIR = resolver_directorio("Queries", "queries")
RESULTADOS_DIR = resolver_directorio("Resultados", "resultados")


def main():
    RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)

    if not QUERIES_DIR.exists():
        print(f"⚠️  No encontré la carpeta '{QUERIES_DIR}'. Créala y pon ahí tus archivos .sql")
        return

    archivos_sql = sorted(QUERIES_DIR.glob("*.sql"))

    if not archivos_sql:
        print(f"⚠️  No hay archivos .sql dentro de '{QUERIES_DIR}'")
        return

    conn = sqlite3.connect(DB_PATH)

    for archivo in archivos_sql:
        nombre_base = archivo.stem  # ej. "query5_algo_nuevo"
        query_sql = archivo.read_text(encoding="utf-8")

        try:
            df = pd.read_sql_query(query_sql, conn)
        except Exception as e:
            print(f"❌ Error en {archivo.name}: {e}")
            continue

        ruta_salida = RESULTADOS_DIR / f"{nombre_base}.csv"
        df.to_csv(ruta_salida, index=False)

        # Limpieza automática de archivos con el formato legado "_resultado".
        ruta_legacy = RESULTADOS_DIR / f"{nombre_base}_resultado.csv"
        if ruta_legacy.exists():
            ruta_legacy.unlink()

        print(f"✅ {archivo.name} → {ruta_salida} ({len(df)} filas)")

    conn.close()
    print(f"\nListo. Todos los resultados están en la carpeta '{RESULTADOS_DIR.name}/'.")


if __name__ == "__main__":
    main()