/*
================================================================
ANÁLISIS ESTRATÉGICO DE ESTACIONALIDAD DE BAJAS
Fecha: 24 de Mayo, 2024
Autor: [Tu Nombre]
Resultados obtenidos: Junio (13), Enero (8), Julio/Mayo (5)...
================================================================
*/

SELECT
  strftime('%m', fecha_baja) AS mes,
  COUNT(*) AS num_bajas
FROM alumnos
WHERE estado = 'baja'
GROUP BY mes
ORDER BY num_bajas DESC;

/*
----------------------------------------------------------------
HALLAZGOS CLAVE (ANÁLISIS DE DATOS REALES):
----------------------------------------------------------------
1. PICO CRÍTICO EN JUNIO (Mes 06):
   Con 13 bajas, junio es el mes con mayor deserción, representando 
   casi el doble que el siguiente mes más alto. 
   *Interpretación:* Esto coincide con el fin del ciclo escolar o 
   el inicio de las vacaciones de verano. Es nuestra zona de mayor riesgo.

2. IMPACTO DE INICIO DE AÑO (Mes 01):
   Enero registra 8 bajas. Este comportamiento es típico debido a 
   ajustes presupuestarios familiares ("Cuesta de Enero") o cambios 
   de propósito de año nuevo que no se consolidaron.

3. ESTABILIDAD EN CIERRE Y APERTURA (Meses 12 y 09):
   Diciembre y Septiembre son los meses más estables con solo 1 baja. 
   Esto indica que una vez que el alumno pasa el filtro de verano, 
   tiende a comprometerse con el cierre del año natural.

----------------------------------------------------------------
ESTRATEGIA RECOMENDADA PARA GERENCIA:
----------------------------------------------------------------
- CAMPAÑA PREVENTIVA (MAYO): Dado que junio es el mes crítico, se 
  debe implementar una estrategia de retención o beneficios especiales 
  en MAYO para asegurar la continuidad durante el verano.

- REVISIÓN DE INSCRIPCIONES EN ENERO: Evaluar si las bajas de enero 
  son alumnos nuevos que se inscribieron en diciembre/enero o alumnos 
  antiguos que decidieron no continuar tras las fiestas.

- MODELO DE ÉXITO SEPTIEMBRE-DICIEMBRE: Estudiar por qué la retención 
  es tan alta en este periodo para intentar replicar ese nivel de 
  compromiso en el primer semestre del año.
================================================================
*/