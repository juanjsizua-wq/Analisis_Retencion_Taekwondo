"""
Genera automáticamente una gráfica de barras por cada CSV dentro de /resultados,
y las guarda en /visualizaciones.

Funciona de forma genérica: usa la primera columna como categoría (eje) y la
última columna numérica como valor — funciona bien para la mayoría de queries
tipo "categoría + métrica". Si alguna gráfica no se ve como esperabas, siempre
puedes ajustar manualmente ese caso en el script generar_graficas.py original.

Requisitos: pip install pandas matplotlib --break-system-packages

Uso:
    python3 generar_graficas_auto.py
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib.colors as mcolors
import textwrap

BASE_DIR = Path(__file__).resolve().parent


def resolver_directorio(preferido: str, alterno: str) -> Path:
    dir_preferido = BASE_DIR / preferido
    dir_alterno = BASE_DIR / alterno

    if dir_preferido.exists():
        return dir_preferido
    if dir_alterno.exists():
        return dir_alterno
    return dir_preferido


RESULTADOS_DIR = resolver_directorio("Resultados", "resultados")
VISUALIZACIONES_DIR = resolver_directorio("Visualizaciones", "visualizaciones")

COLOR_PRINCIPAL = "#4E79A7"
COLOR_SECUNDARIO = "#F28E2B"
COLOR_ALERTA = "#E15759"
COLOR_BUENO = "#59A14F"
COLOR_NEUTRO = "#76B7B2"
MAX_FILAS_GRAFICA = 15
MAX_FILAS_QUERY5 = 10

plt.rcParams["font.size"] = 11
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.facecolor"] = "#FAFAFA"
plt.rcParams["figure.facecolor"] = "white"


def elegir_columnas(df):
    """Elige la primera columna como categoría y la última numérica como valor."""
    columnas_numero = df.select_dtypes(include="number").columns.tolist()

    if df.empty or not columnas_numero:
        return None, None

    return df.columns[0], columnas_numero[-1]


def construir_etiquetas(df, col_categoria):
    """Construye etiquetas más únicas usando todas las columnas de texto disponibles."""
    columnas_texto = df.select_dtypes(include="object").columns.tolist()
    if not columnas_texto:
        return df[col_categoria].astype(str)

    etiquetas = df[columnas_texto].astype(str).agg(" | ".join, axis=1)
    return etiquetas


def construir_etiqueta_query5(df):
    """Etiqueta compacta para la Query 5: solo alumno y contexto breve."""
    columnas = df.columns.tolist()
    if "id_alumno" in columnas:
        etiqueta = df["id_alumno"].astype(str)
        if "colegio" in columnas:
            etiqueta = etiqueta + " • " + df["colegio"].astype(str)
        if "dia_horario" in columnas:
            etiqueta = etiqueta + " • " + df["dia_horario"].astype(str)
        return etiqueta
    return df.iloc[:, 0].astype(str)


def titular(nombre_base):
    if nombre_base.startswith("query"):
        numero = nombre_base.split("_", 1)[0].replace("query", "")
        resto = nombre_base.split("_", 1)[1] if "_" in nombre_base else nombre_base
        return numero, resto.replace("_", " ").title()
    return "", nombre_base.replace("_", " ").title()


def abreviar_texto(valor, max_len=26):
    texto = str(valor)
    if len(texto) <= max_len:
        return texto
    return "\n".join(textwrap.wrap(texto, width=max_len, break_long_words=False))


def color_por_valor(serie):
    if serie.empty:
        return [COLOR_PRINCIPAL]
    minimo = float(serie.min())
    maximo = float(serie.max())
    if minimo == maximo:
        return [COLOR_PRINCIPAL for _ in serie]
    cmap = mcolors.LinearSegmentedColormap.from_list(
        "retencion",
        [COLOR_ALERTA, COLOR_SECUNDARIO, COLOR_BUENO],
    )
    normalizador = mcolors.Normalize(vmin=minimo, vmax=maximo)
    return [cmap(normalizador(valor)) for valor in serie]


def preparar_datos(df, col_categoria, col_valor):
    df = df.copy()
    df["_etiqueta"] = construir_etiquetas(df, col_categoria)

    if df["_etiqueta"].duplicated().any():
        df = df.groupby("_etiqueta", as_index=False)[col_valor].mean()
    else:
        df = df[["_etiqueta", col_valor]]

    df = df.dropna(subset=[col_valor])
    df = df.sort_values(col_valor, ascending=False)
    return df


def graficar_por_tipo(ax, nombre_base, df, col_valor):
    nombre_numero, titulo = titular(nombre_base)
    etiquetas = df["_etiqueta"].astype(str).map(abreviar_texto)
    valores = df[col_valor]

    if "bajas_por_mes" in nombre_base and "mes" in " ".join(etiquetas).lower():
        etiquetas_x = etiquetas
        colores = color_por_valor(valores)
        ax.plot(etiquetas_x, valores, color=COLOR_PRINCIPAL, marker="o", linewidth=2.5)
        ax.fill_between(range(len(valores)), valores.values, color=COLOR_PRINCIPAL, alpha=0.12)
        ax.scatter(etiquetas_x, valores, c=colores, s=85, edgecolors="white", linewidths=1.2, zorder=3)
        for x, y in zip(etiquetas_x, valores):
            ax.text(x, y + (valores.max() * 0.03), f"{y}", ha="center", va="bottom", fontsize=10, fontweight="bold")
        ax.set_ylabel(col_valor.replace("_", " "))
        ax.grid(axis="y", alpha=0.18)
        ax.margins(x=0.02)
        ax.tick_params(axis="x", rotation=0)
        return titulo, nombre_numero

    if len(df) == 2:
        colores = [COLOR_ALERTA, COLOR_BUENO]
        wedges, texts, autotexts = ax.pie(
            valores,
            labels=etiquetas,
            autopct=lambda pct: f"{pct:.1f}%",
            startangle=90,
            colors=colores,
            wedgeprops={"width": 0.42, "edgecolor": "white"},
            textprops={"fontsize": 11, "fontweight": "bold"},
        )
        for autotext in autotexts:
            autotext.set_color("#222222")
        ax.set_aspect("equal")
        return titulo, nombre_numero

    if len(df) <= 6:
        colores = [COLOR_ALERTA, COLOR_SECUNDARIO, COLOR_BUENO, COLOR_NEUTRO, COLOR_PRINCIPAL, "#B07AA1"]
        colores = colores[:len(df)]
        bars = ax.bar(etiquetas, valores, color=colores, edgecolor="white", linewidth=1.1)
        for bar, val in zip(bars, valores):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (valores.max() * 0.03),
                    f"{val}", ha="center", va="bottom", fontweight="bold", fontsize=10)
        ax.set_ylabel(col_valor.replace("_", " "))
        ax.grid(axis="y", alpha=0.18)
        ax.tick_params(axis="x", rotation=20)
        return titulo, nombre_numero

    colores = color_por_valor(valores)
    bars = ax.bar(etiquetas, valores, color=colores, edgecolor="white", linewidth=1.0)
    for bar, val in zip(bars, valores):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (valores.max() * 0.02),
                f"{val}", ha="center", va="bottom", fontweight="bold", fontsize=9)
    ax.set_ylabel(col_valor.replace("_", " "))
    ax.grid(axis="y", alpha=0.18)
    ax.tick_params(axis="x", rotation=45)
    return titulo, nombre_numero


def aplicar_estilo_ejecutivo(ax):
    ax.grid(axis="x", alpha=0.18)
    ax.set_axisbelow(True)
    ax.spines["left"].set_alpha(0.2)
    ax.spines["bottom"].set_alpha(0.2)


def main():
    VISUALIZACIONES_DIR.mkdir(parents=True, exist_ok=True)

    # Dejar solo las gráficas actuales: borramos cualquier PNG previo antes de regenerar.
    for archivo_png in VISUALIZACIONES_DIR.glob("*.png"):
        archivo_png.unlink()

    if not RESULTADOS_DIR.exists():
        print(f"⚠️  No encontré la carpeta '{RESULTADOS_DIR}'. Corre primero correr_queries.py")
        return

    archivos_csv = sorted(RESULTADOS_DIR.glob("*.csv"))

    if not archivos_csv:
        print(f"⚠️  No hay archivos CSV dentro de '{RESULTADOS_DIR}'")
        return

    for archivo in archivos_csv:
        nombre_base = archivo.stem
        df = pd.read_csv(archivo)
        df_original = df.copy()

        col_categoria, col_valor = elegir_columnas(df)
        if col_categoria is None:
            print(f"⚠️  {archivo.name}: no pude detectar columnas de categoría/valor automáticamente, sáltalo")
            continue

        df = preparar_datos(df, col_categoria, col_valor)
        df_ordenado = df.copy()
        recortado = False

        if len(df_ordenado) > MAX_FILAS_GRAFICA:
            df_ordenado = df_ordenado.head(MAX_FILAS_GRAFICA).sort_values(col_valor, ascending=True)
            recortado = True
        else:
            df_ordenado = df_ordenado.sort_values(col_valor, ascending=True)

        numero_query, titulo_base = titular(nombre_base)

        if nombre_base == "query1_bajas_tempranas":
            fig, ax = plt.subplots(figsize=(7.5, 5.8))
            colores = [COLOR_ALERTA, COLOR_BUENO][:len(df_ordenado)]
            wedges, texts, autotexts = ax.pie(
                df_ordenado[col_valor],
                autopct=lambda pct: f"{pct:.1f}%",
                startangle=90,
                colors=colores,
                wedgeprops={"width": 0.42, "edgecolor": "white"},
                textprops={"fontsize": 11, "fontweight": "bold"},
            )
            for autotext in autotexts:
                autotext.set_color("#222222")
            ax.set_aspect("equal")
            ax.set_title(f"{numero_query}. {titulo_base}", fontsize=14, fontweight="bold", pad=15)
            ax.legend(
                wedges,
                df_ordenado["_etiqueta"].astype(str),
                loc="upper center",
                bbox_to_anchor=(0.5, -0.04),
                ncol=1,
                frameon=False,
                fontsize=10,
            )
        elif nombre_base == "query2_retencion_por_grupo":
            fig, ax = plt.subplots(figsize=(9, 6))
            colores = color_por_valor(df_ordenado[col_valor])
            bars = ax.bar(df_ordenado["_etiqueta"].astype(str), df_ordenado[col_valor], color=colores, edgecolor="white", linewidth=1.1)
            for bar, val in zip(bars, df_ordenado[col_valor]):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (df_ordenado[col_valor].max() * 0.02),
                        f"{val}%", ha="center", va="bottom", fontweight="bold", fontsize=10)
            ax.set_title(f"{numero_query}. {titulo_base}", fontsize=14, fontweight="bold", pad=15)
            ax.set_ylabel(col_valor.replace("_", " "))
            ax.set_ylim(0, max(100, df_ordenado[col_valor].max() + 10))
            ax.axhline(df_ordenado[col_valor].mean(), color=COLOR_SECUNDARIO, linestyle="--", linewidth=1.3, alpha=0.85)
            ax.grid(axis="y", alpha=0.18)
            ax.tick_params(axis="x", rotation=25)
        elif nombre_base == "query3_bajas_por_mes":
            fig, ax = plt.subplots(figsize=(9, 5.5))
            colores = [COLOR_ALERTA, COLOR_SECUNDARIO, COLOR_BUENO, COLOR_NEUTRO, COLOR_PRINCIPAL, "#B07AA1", "#EDC948", "#FF9DA7", "#9C755F", "#BAB0AC", "#86BCB6", "#D37295"]
            colores = colores[:len(df_ordenado)]
            bars = ax.bar(df_ordenado["_etiqueta"].astype(str), df_ordenado[col_valor], color=colores, edgecolor="white", linewidth=1.0)
            for bar, val in zip(bars, df_ordenado[col_valor]):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (df_ordenado[col_valor].max() * 0.03),
                        f"{val}", ha="center", va="bottom", fontweight="bold", fontsize=10)
            ax.set_title(f"{numero_query}. {titulo_base}", fontsize=14, fontweight="bold", pad=15)
            ax.set_ylabel(col_valor.replace("_", " "))
            ax.grid(axis="y", alpha=0.18)
            ax.tick_params(axis="x", rotation=0)
        elif nombre_base == "query4_asistencia_antes_de_baja":
            fig, ax = plt.subplots(figsize=(8.5, 5.5))
            colores = [COLOR_ALERTA if i == 0 else COLOR_BUENO for i in range(len(df_ordenado))]
            bars = ax.bar(df_ordenado["_etiqueta"].astype(str), df_ordenado[col_valor], color=colores, edgecolor="white", linewidth=1.1)
            for bar, val in zip(bars, df_ordenado[col_valor]):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (df_ordenado[col_valor].max() * 0.02),
                        f"{val}%", ha="center", va="bottom", fontweight="bold", fontsize=10)
            ax.set_title(f"{numero_query}. {titulo_base}", fontsize=14, fontweight="bold", pad=15)
            ax.set_ylabel(col_valor.replace("_", " "))
            ax.set_ylim(0, 100)
            ax.grid(axis="y", alpha=0.18)
            ax.tick_params(axis="x", rotation=18)
        elif nombre_base == "query5_pagos_atrasados":
            df_query5 = df_original.copy()
            df_query5["_etiqueta"] = construir_etiqueta_query5(df_query5)
            df_query5 = df_query5.sort_values(col_valor, ascending=False).head(MAX_FILAS_QUERY5)

            fig, ax = plt.subplots(figsize=(10.5, 6.3))
            colores = color_por_valor(df_query5[col_valor])
            bars = ax.barh(df_query5["_etiqueta"].astype(str), df_query5[col_valor], color=colores, edgecolor="white", linewidth=1.0)

            for bar, (_, fila) in zip(bars, df_query5.iterrows()):
                ax.text(
                    bar.get_width() + (df_query5[col_valor].max() * 0.02),
                    bar.get_y() + bar.get_height() / 2,
                    f"MXN {fila[col_valor]:,.0f} | {fila['num_pagos_atrasados']} pagos",
                    ha="left",
                    va="center",
                    fontweight="bold",
                    fontsize=9,
                )

            ax.set_title(f"{numero_query}. {titulo_base} - Top {MAX_FILAS_QUERY5}", fontsize=14, fontweight="bold", pad=15)
            ax.set_xlabel("Monto total atrasado (MXN)")
            aplicar_estilo_ejecutivo(ax)
            ax.invert_yaxis()
        else:
            fig, ax = plt.subplots(figsize=(max(8, len(df_ordenado) * 0.7), 6))
            bars = ax.bar(df_ordenado["_etiqueta"].astype(str), df_ordenado[col_valor], color=COLOR_PRINCIPAL, edgecolor="white", linewidth=1.0)
            for bar, val in zip(bars, df_ordenado[col_valor]):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (df_ordenado[col_valor].max() * 0.02),
                        f"{val}", ha="center", va="bottom", fontweight="bold", fontsize=10)
            ax.set_title(f"{numero_query}. {titulo_base}", fontsize=14, fontweight="bold", pad=15)
            ax.set_ylabel(col_valor.replace("_", " "))
            ax.grid(axis="y", alpha=0.18)
            ax.tick_params(axis="x", rotation=45)

        plt.tight_layout()

        nombre_png = nombre_base.replace("query", "grafica", 1) if nombre_base.startswith("query") else f"grafica_{nombre_base}"
        ruta_salida = VISUALIZACIONES_DIR / f"{nombre_png}.png"
        plt.savefig(ruta_salida, dpi=150)
        plt.close()
        ruta_legacy = VISUALIZACIONES_DIR / f"{nombre_base}.png"
        if ruta_legacy.exists() and ruta_legacy != ruta_salida:
            ruta_legacy.unlink()

        if recortado:
            print(f"✅ {archivo.name} → {ruta_salida} (graficadas solo {MAX_FILAS_GRAFICA} filas de {len(df)})")
        else:
            print(f"✅ {archivo.name} → {ruta_salida}")

    print("\nListo. Revisa las gráficas en 'visualizaciones/' — las genéricas se ven bien,")
    print("pero para tus 4 gráficas principales sigue usando generar_graficas.py (más personalizado).")


if __name__ == "__main__":
    main()