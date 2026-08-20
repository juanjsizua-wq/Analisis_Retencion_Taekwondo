/*
================================================================
ANÁLISIS FINANCIERO: PAGOS ATRASADOS POR ALUMNO
Fecha: 19 de Agosto, 2026
Autor: Juan Jesus Sifuentes
Descripción: Reporte de cartera vencida para identificar alumnos
						 con mayor riesgo financiero y priorizar seguimiento.
================================================================
*/

WITH pagos_atrasados AS (
	SELECT
		m.id_alumno,
		m.mes_pagado,
		CAST(m.monto AS REAL) AS monto
	FROM mensualidades m
	WHERE LOWER(TRIM(REPLACE(m.estatus, char(13), ''))) = 'atrasado'
)
SELECT
	pa.id_alumno,
	a.colegio,
	g.dia_horario,
	COUNT(*) AS num_pagos_atrasados,
	ROUND(SUM(pa.monto), 2) AS monto_total_atrasado,
	MIN(pa.mes_pagado) AS mes_mas_antiguo_atrasado,
	MAX(pa.mes_pagado) AS mes_mas_reciente_atrasado,
	-- Antigüedad del adeudo desde el mes más antiguo en atraso
	((CAST(strftime('%Y', 'now') AS INTEGER) - CAST(substr(MIN(pa.mes_pagado), 1, 4) AS INTEGER)) * 12
	 + (CAST(strftime('%m', 'now') AS INTEGER) - CAST(substr(MIN(pa.mes_pagado), 6, 2) AS INTEGER))) AS meses_de_antiguedad
FROM pagos_atrasados pa
JOIN alumnos a ON pa.id_alumno = a.id_alumno
LEFT JOIN grupos g ON a.id_grupo = g.id_grupo
GROUP BY pa.id_alumno, a.colegio, g.dia_horario
ORDER BY monto_total_atrasado DESC, num_pagos_atrasados DESC;

/*
----------------------------------------------------------------
INTERPRETACIÓN RÁPIDA:
----------------------------------------------------------------
- num_pagos_atrasados: cuántas mensualidades vencidas tiene el alumno.
- monto_total_atrasado: deuda acumulada total en moneda del dataset.
- meses_de_antiguedad: qué tan vieja es la deuda más antigua.

USO SUGERIDO:
- Priorizar cobranza por monto_total_atrasado y meses_de_antiguedad.
- Cruzar con estado del alumno para campañas de recuperación.
================================================================
*/
