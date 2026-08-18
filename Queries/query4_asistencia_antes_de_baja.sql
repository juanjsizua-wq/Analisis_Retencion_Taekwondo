/*
================================================================
ANÁLISIS PREDICTIVO: ASISTENCIA VS. DESERCIÓN
Fecha: 18 de Agosto, 2026
Autor: Juan Jesus Sifuentes
Descripción: Comparativa del rendimiento de asistencia en el 
             último mes de vida del alumno vs. su histórico.
================================================================
*/
SELECT
  CASE
    WHEN julianday(a.fecha_inscripcion) IS NOT NULL
     AND a.fecha_baja != ''
     AND julianday(a.fecha_baja) - julianday(asis.fecha_clase) <= 28
    THEN 'Últimas 4 semanas antes de la baja'
    ELSE 'Resto del periodo'
  END AS periodo,
  ROUND(SUM(CASE WHEN asis.presente = 'si' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS pct_asistencia
FROM asistencia asis
JOIN alumnos a ON asis.id_alumno = a.id_alumno
WHERE a.estado = 'baja'
GROUP BY periodo;

/*
----------------------------------------------------------------
HALLAZGOS CLAVE (INDICADORES TEMPRANOS):
----------------------------------------------------------------
1. COMPORTAMIENTO HISTÓRICO (83.0%):
   Un alumno que termina dándose de baja, solía tener una asistencia 
   saludable del 83%. Esto indica que no eran "malos alumnos" desde 
   el principio, sino que algo cambió en su motivación o situación.

2. EL "SÍNTOMA" DE DESERCIÓN (45.7%):
   En las últimas 4 semanas previas a la baja formal, la asistencia 
   desciende drásticamente a menos de la mitad (45.7%).
   
3. VENTANA DE INTERVENCIÓN:
   Los datos demuestran que la baja no es una decisión repentina; 
   hay un periodo de "desconexión" de aproximadamente un mes donde 
   el alumno deja de asistir antes de avisar oficialmente.

----------------------------------------------------------------
ESTRATEGIA DE RETENCIÓN PROPUESTA:
----------------------------------------------------------------
- ALERTAS AUTOMATIZADAS: Establecer una alerta roja cuando la 
  asistencia mensual de un alumno caiga por debajo del 60%. 
  Basado en este análisis, ese alumno tiene una alta probabilidad 
  de darse de baja en los próximos 30 días.

- PROTOCOLO DE RECUPERACIÓN: Si un alumno falta a 2 clases 
  consecutivas, realizar una llamada de seguimiento inmediata. 
  Actualmente, tenemos una ventana de 4 semanas para "re-enamorar" 
  al alumno antes de perderlo definitivamente.

- CONCLUSIÓN: La asistencia es nuestro mejor termómetro. Si logramos 
  atender la caída del 83% al 45%, reduciremos drásticamente 
  la tasa de bajas anuales.
================================================================
*/
