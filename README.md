# Analisis_Retencion_Taekwondo
Análisis de retención de alumnos en academia de Taekwondo usando SQL — datos simulados con esquema relacional (Star Schema)
# 📊 Análisis de Retención y Deserción de Alumnos

## 🎯 El Problema: ¿Por qué importa la retención?
Para una institución educativa, la retención de alumnos es el indicador más crítico de salud operativa. Una baja tasa de retención no solo afecta los ingresos, sino que incrementa los costos de adquisición de nuevos alumnos y rompe la continuidad pedagógica de los grupos. 

Este análisis busca identificar los **patrones de abandono** para transformar datos históricos en estrategias preventivas que aseguren la estabilidad de la academia.

---

## 🔍 Preguntas de Negocio
Para entender el fenómeno de la deserción, este análisis responde a cuatro preguntas clave:
1. **¿Qué tan rápido perdemos a los alumnos?** (Periodo crítico de 90 días).
2. **¿Qué grupos y horarios presentan mayor riesgo?** (Análisis por sede y horario).
3. **¿Existe una estacionalidad en las bajas?** (Meses con mayor índice de fuga).
4. **¿Podemos predecir una baja antes de que ocurra?** (Correlación entre asistencia y deserción).

---

## 📈 Hallazgos Clave

### 1. Clasificación del "Churn" (Bajas Tempranas vs. Tardías)
Se analizó el tiempo transcurrido entre la inscripción y la baja, utilizando un umbral de 90 días para identificar problemas de adaptación inicial.
*   **Hallazgo:** La segmentación permite identificar si el problema radica en el proceso de bienvenida (*onboarding*) o en el desgaste a largo plazo del contenido académico.

### 2. Rendimiento por Grupo y Sede
Cruzamos el estado de los alumnos con su asignación de grupo para medir el porcentaje de retención real.
*   **Hallazgo:** El grupo de **Sábados 10:00 AM (Colegio A)** lidera la retención con un **90.9%**. En contraste, los horarios de las **4:00 PM** en ambas sedes muestran una retención crítica de apenas el **60%**, siendo el punto de mayor vulnerabilidad.

### 3. Análisis de Estacionalidad
Se extrajo el mes de cada baja para identificar picos de deserción durante el año natural.
*   **Hallazgo:** **Junio** es el mes con mayor volumen de bajas (13), seguido de **Enero** (8). Esto sugiere una dependencia directa del calendario escolar y de los periodos de ajustes económicos familiares.

### 4. El Indicador Predictivo: Asistencia
Comparamos la asistencia histórica del alumno contra su comportamiento en las últimas 4 semanas antes de abandonar.
*   **Hallazgo:** Un alumno que se dará de baja reduce su asistencia del **83% al 45.7%** un mes antes de formalizar su salida. **La inasistencia es el síntoma principal y nos otorga una ventana de intervención de 28 días.**

---

## 💡 Conclusiones Accionables

Basado en la evidencia obtenida mediante SQL, se proponen las siguientes acciones:

1.  **Protocolo de Alerta Roja:** Activar un contacto inmediato de "recuperación" cuando la asistencia mensual de un alumno caiga por debajo del 60%. Es posible salvar casi al 50% de los desertores si se interviene en este periodo.
2.  **Blindaje de Temporada Alta:** Implementar campañas de lealtad o beneficios de reinscripción en **Mayo y Diciembre** para mitigar las fugas masivas de Junio y Enero.
3.  **Revisión del Bloque de las 4:00 PM:** Evaluar si el bajo rendimiento en este horario se debe a fatiga escolar o factores logísticos, considerando mover la oferta académica hacia las 6:00 PM, donde los datos muestran una retención más sólida.
4.  **Refuerzo en los primeros 90 días:** Establecer entrevistas de seguimiento al finalizar el primer y segundo mes para asegurar que el alumno supere la etapa de "Baja Temprana".

---

## 🛠️ Tecnologías y Metodología
*   **SQL (SQLite):** Consultas avanzadas utilizando `strftime`, `julianday`, subconsultas y lógica condicional `CASE`.
*   **Análisis de Datos:** Enfoque en métricas de retención (*Retention Rate*) y tasa de cancelación (*Churn Rate*).
