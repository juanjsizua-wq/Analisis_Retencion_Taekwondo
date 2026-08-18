--Pregunta 1: ¿Qué % de alumnos se da de baja en los primeros 3 meses vs. después?
/*
================================================================
ANÁLISIS DE TEMPORALIDAD DE BAJAS (CHURN RATE)
Fecha: 24 de Mayo, 2024
Autor: Juan Jesus Sifuentes
Descripción: Clasificación de bajas en "Tempranas" vs "Tardías" 
             para medir la eficacia del periodo de adaptación.
================================================================
*/

SELECT
  CASE
   -- Definimos 90 días como el periodo crítico de adaptación (3 meses)
    WHEN julianday(fecha_baja) - julianday(fecha_inscripcion) <= 90 THEN 'Baja temprana (0-3 meses)'
    ELSE 'Baja tardía (más de 3 meses)'
  END AS tipo_baja,
  COUNT(*) AS num_alumnos,
  -- Cálculo de impacto porcentual sobre el total de desertores
  ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM alumnos WHERE estado = 'baja'), 1) AS porcentaje
FROM alumnos
WHERE estado = 'baja'
GROUP BY tipo_baja;

/*
----------------------------------------------------------------
INTERPRETACIÓN DE MÉTRICAS (GUÍA PARA GERENCIA):
----------------------------------------------------------------
1. BAJA TEMPRANA (0-3 MESES):
   Si este porcentaje es elevado (>30%), indica problemas en:
   - El proceso de inscripción o expectativas mal gestionadas.
   - La calidad de las clases en los niveles introductorios.
   - Falta de acompañamiento en el primer mes del alumno.

2. BAJA TARDÍA (>3 MESES):
   Si este porcentaje es el dominante, indica:
   - Desgaste natural o finalización de ciclos.
   - Factores externos (cambios de domicilio, situación económica).
   - Necesidad de renovar la oferta académica para mantener el interés.

----------------------------------------------------------------
ACCIONES SUGERIDAS:
----------------------------------------------------------------
- Realizar "Entrevistas de Salida" obligatorias a quienes se den 
  de baja antes de los 90 días.
- Implementar un sistema de "Check-in" al segundo mes para detectar 
  alumnos en riesgo antes de que cumplan el trimestre.
================================================================
*/