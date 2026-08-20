"""
Genera las 4 gráficas del análisis de retención de alumnos a partir
de los CSV con resultados de las queries SQL.

Requisitos: pip install pandas matplotlib --break-system-packages

Coloca este script en la misma carpeta donde tienes:
los resultados CSV dentro de /Resultados con nombres como:
query1_bajas_tempranas.csv, query2_retencion_por_grupo.csv, etc.

Uso:
    python3 generar_graficas.py
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Paleta de colores consistente
COLOR_ALERTA = "#E15759"   # rojo/naranja - para lo que indica riesgo
COLOR_NEUTRO = "#4E79A7"   # azul - para lo neutro/bueno
COLOR_BUENO = "#59A14F"    # verde - para lo positivo

plt.rcParams["font.size"] = 11
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False

# Rutas del proyecto para no depender del directorio actual
BASE_DIR = Path(__file__).resolve().parent.parent
RESULTADOS_DIR = BASE_DIR / "Resultados"
VISUALIZACIONES_DIR = BASE_DIR / "Visualizaciones"
VISUALIZACIONES_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------------
# GRÁFICA 1: Bajas tempranas vs. tardías
# ------------------------------------------------------------------
df1 = pd.read_csv(RESULTADOS_DIR / "query1_bajas_tempranas.csv")

fig, ax = plt.subplots(figsize=(7, 5))
colores = [COLOR_ALERTA if "temprana" in t.lower() else COLOR_NEUTRO for t in df1["tipo_baja"]]
bars = ax.bar(df1["tipo_baja"], df1["porcentaje"], color=colores)

for bar, val in zip(bars, df1["porcentaje"]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
            f"{val}%", ha="center", fontweight="bold", fontsize=12)

ax.set_title("% de Bajas Tempranas vs. Tardías", fontsize=14, fontweight="bold", pad=15)
ax.set_ylabel("% de bajas")
ax.set_ylim(0, max(df1["porcentaje"]) + 10)
plt.tight_layout()
plt.savefig(VISUALIZACIONES_DIR / "grafica1_bajas_tempranas.png", dpi=150)
plt.close()
print("✅ grafica1_bajas_tempranas.png")


# ------------------------------------------------------------------
# GRÁFICA 2: Retención por horario/grupo
# ------------------------------------------------------------------
df2 = pd.read_csv(RESULTADOS_DIR / "query2_retencion_por_grupo.csv")
df2 = df2.sort_values("pct_retencion", ascending=True)  # ascending para que barh se vea de mayor arriba

fig, ax = plt.subplots(figsize=(8, 5))
colores2 = [COLOR_BUENO if v >= 70 else COLOR_ALERTA if v < 62 else COLOR_NEUTRO
            for v in df2["pct_retencion"]]
bars = ax.barh(df2["dia_horario"], df2["pct_retencion"], color=colores2)

for bar, val in zip(bars, df2["pct_retencion"]):
    ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
            f"{val}%", va="center", fontweight="bold", fontsize=11)

ax.set_title("% de Retención de Alumnos por Horario", fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("% de Retención")
ax.set_xlim(0, 100)
plt.tight_layout()
plt.savefig(VISUALIZACIONES_DIR / "grafica2_retencion_horario.png", dpi=150)
plt.close()
print("✅ grafica2_retencion_horario.png")


# ------------------------------------------------------------------
# GRÁFICA 3: Bajas por mes
# ------------------------------------------------------------------
df3 = pd.read_csv(RESULTADOS_DIR / "query3_bajas_por_mes.csv")

MESES = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
         7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"}
df3["mes_nombre"] = df3["mes"].astype(int).map(MESES)
df3 = df3.sort_values("mes")

fig, ax = plt.subplots(figsize=(8, 5))
colores3 = [COLOR_ALERTA if m in [1, 6] else COLOR_NEUTRO for m in df3["mes"]]
bars = ax.bar(df3["mes_nombre"], df3["num_bajas"], color=colores3)

for bar, val in zip(bars, df3["num_bajas"]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
            f"{val}", ha="center", fontweight="bold", fontsize=11)

ax.set_title("Número de Bajas por Mes", fontsize=14, fontweight="bold", pad=15)
ax.set_ylabel("Número de bajas")
plt.tight_layout()
plt.savefig(VISUALIZACIONES_DIR / "grafica3_bajas_por_mes.png", dpi=150)
plt.close()
print("✅ grafica3_bajas_por_mes.png")


# ------------------------------------------------------------------
# GRÁFICA 4: Asistencia antes de la baja
# ------------------------------------------------------------------
df4 = pd.read_csv(RESULTADOS_DIR / "query4_asistencia_antes_de_baja.csv")

fig, ax = plt.subplots(figsize=(7, 5))
colores4 = [COLOR_ALERTA if "ultimas" in p.lower() or "últimas" in p.lower() else COLOR_NEUTRO
            for p in df4["periodo"]]
bars = ax.bar(df4["periodo"], df4["pct_asistencia"], color=colores4)

for bar, val in zip(bars, df4["pct_asistencia"]):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
            f"{val}%", ha="center", fontweight="bold", fontsize=12)

ax.set_title("% de Asistencia Antes de una Baja\n(señal de alerta temprana)",
             fontsize=14, fontweight="bold", pad=15)
ax.set_ylabel("% de asistencia")
ax.set_ylim(0, 100)
plt.tight_layout()
plt.savefig(VISUALIZACIONES_DIR / "grafica4_asistencia_alerta.png", dpi=150)
plt.close()
print("✅ grafica4_asistencia_alerta.png")

print(f"\nListo. Las 4 gráficas quedaron guardadas en: {VISUALIZACIONES_DIR}")