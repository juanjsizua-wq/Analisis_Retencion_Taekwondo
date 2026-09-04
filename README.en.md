# 🥋 Student Retention Analysis — Taekwondo Academy

Data Analysis portfolio project: I identify retention and dropout patterns among
students in a Taekwondo academy using SQL, Python, and data visualization.

> **Note on the data**: to protect the privacy of minors, this project uses
> **simulated** data that replicates realistic patterns of a real academy (based
> on my 10 years of experience as an instructor), not information from real students.

---

## 📌 The problem

As a Taekwondo instructor, one of the most important questions for the business is:
**why do students drop out, and can it be anticipated?** This project uses
enrollment, attendance, and payment data to answer that question with evidence,
not just intuition.

---

## 🗂️ Data structure

The dataset follows a relational (Star) schema with 6 tables:

| Table | Type | Description |
|---|---|---|
| `alumnos` | Dimension | One record per student: enrollment, status, dropout |
| `grupos` | Dimension | Catalog of schedules and schools |
| `torneos` | Dimension | Catalog of events/tournaments |
| `asistencia` | Fact | One record per class per student |
| `mensualidades` | Fact | Payment history |
| `participacion_torneos` | Fact | Which student attended which tournament |

---

## 🛠️ Methodology

1. **Simulated data generation** with Python (`generar_datos.py`), respecting
   realistic relationships and patterns
2. **Load into SQLite** (`cargar_db.py`) to query with SQL
3. **4 business questions** answered with SQL queries (`/queries` folder)
4. **Visualization** of results with Python/matplotlib (`generar_graficas.py`)
5. Automated pipeline (`correr_queries.py` + `generar_graficas_auto.py`) to add new
   questions without repeating manual work

---

## 📊 Key findings

### 1. 39.5% of dropouts happen in the first 3 months

![Early dropouts](Visualizaciones/grafica1_bajas_tempranas.png?v=ea6106a)

Nearly 4 out of every 10 students who drop out do so before reaching 90 days.
**Recommendation**: active follow-up with parents in the first 4-8 weeks, the
highest-risk period.

### 2. 4:00pm schedules retain 30 points less than Saturdays

![Retention by schedule](Visualizaciones/grafica2_retencion_por_grupo.png)

Saturday 10am has 90.9% retention vs. 59-60% for weekday 4pm schedules, likely due
to fatigue after the school day. **Recommendation**: evaluate moving 4pm groups to
later time slots when operationally feasible.

### 3. January and June concentrate the most dropouts

![Dropouts by month](Visualizaciones/grafica3_bajas_por_mes.png)

This coincides with the return from winter break and the end of the school year.
**Recommendation**: reminder/re-enrollment campaigns 2 weeks before these periods,
instead of reacting afterward.

### 4. Attendance drops before a dropout — an early warning signal

![Attendance before dropout](Visualizaciones/grafica4_asistencia_antes_de_baja.png)

In the last 4 weeks before dropping out, attendance drops noticeably. This makes
attendance a **predictive indicator**, not just a descriptive one.
**Recommendation**: a simple alert system (2+ absences in 2 weeks → direct contact)
could anticipate dropouts before they happen.

📄 **See the full analysis with context and detailed recommendations**:
[insights/hallazgos_y_recomendaciones.md](insights/hallazgos_y_recomendaciones.md)

---

## 📁 Repository structure

```
analisis-retencion-taekwondo/
├── README.md
├── generar_datos.py              # generates the simulated data
├── cargar_db.py                  # loads the CSVs into SQLite
├── correr_queries.py             # automatically runs all queries
├── generar_graficas.py           # main charts (4 findings)
├── generar_graficas_auto.py      # automatic charts for new queries
├── taekwondo.db
├── data/                         # simulated data (6 tables)
├── queries/                      # .sql files for each question
├── resultados/                   # results of each query in CSV
├── Visualizaciones/               # PNG charts
└── insights/                     # extended analysis with recommendations
```

---

## 🧰 Tools used

SQL (SQLite) · Python (pandas, matplotlib) · Relational modeling (Star Schema) · Git/GitHub

---

## 📫 Contact

- LinkedIn: [https://www.linkedin.com/in/juan-jesus-sifuentes-zuazua-a8600a240/]
- GitHub: [github.com/juanjsizua-wq](https://github.com/juanjsizua-wq)
