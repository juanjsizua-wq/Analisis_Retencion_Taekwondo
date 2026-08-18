--Pregunta 2: ¿Qué horario/grupo tiene mejor retención?
/*
================================================================                
ANÁLISIS DE RETENCIÓN POR GRUPO Y COLEGIO
Fecha: 18 de Agosto, 2026
Autor: Juan Jesus Sifuentes 
Descripción: Evaluación de la salud de los grupos basada en el 
             porcentaje de alumnos activos vs. inscripciones totales.
================================================================
*/

SELECT
  g.dia_horario,
  g.colegio,
  COUNT(a.id_alumno) AS total_alumnos,
  SUM(CASE WHEN a.estado = 'activo' THEN 1 ELSE 0 END) AS activos,
  ROUND(SUM(CASE WHEN a.estado = 'activo' THEN 1 ELSE 0 END) * 100.0 / COUNT(a.id_alumno), 1) AS pct_retencion
FROM alumnos a
JOIN grupos g ON a.id_grupo = g.id_grupo
GROUP BY g.id_grupo
ORDER BY pct_retencion DESC;

/*
----------------------------------------------------------------
OBSERVACIONES CLAVE (HALLAZGOS):
----------------------------------------------------------------
1. ÉXITO EN SÁBADOS: 
   El grupo de Sábado 10:00am (Colegio A) lidera la retención con un 90.9%.
   Los fines de semana presentan una estabilidad superior a los grupos de diario.

2. PUNTO DE FUGA (4:00 PM):
   Se detectó que la retención más baja ocurre en el bloque de las 4:00pm
   tanto en el Colegio A (60.0%) como en el Colegio B (59.1%).
   *Hipótesis:* Posible conflicto con horarios escolares o fatiga de los alumnos.

3. VOLUMEN CRÍTICO:
   El grupo Lun-Mie 6:00pm es el que más alumnos ha procesado (29),
   pero su tasa de retención (65.5%) sugiere una rotación constante que
   incrementa el costo de adquisición de alumnos.

----------------------------------------------------------------
RECOMENDACIONES:
----------------------------------------------------------------
- Realizar encuestas de salida específicas para los grupos de las 4:00pm.
- Evaluar la apertura de nuevas secciones los sábados por la mañana.
- Entrevistar al instructor del grupo Sábado 10:00am para replicar su metodología.
================================================================
*/