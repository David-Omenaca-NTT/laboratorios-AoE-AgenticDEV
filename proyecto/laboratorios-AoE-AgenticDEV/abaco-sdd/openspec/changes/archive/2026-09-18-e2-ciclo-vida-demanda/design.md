## Context

No hay sistema previo. La unica fuente hoy son correos y una hoja de calculo
que mantiene una persona. El ciclo de estados sale del PRD de la plataforma y
se conserva tal cual para no inventar vocabulario nuevo al area.

## Goals / Non-Goals

**Goals:**
- Que el estado de una demanda sea un hecho consultable y no una opinion
- Que las transiciones invalidas fallen en el sistema y no en una reunion

**Non-Goals:**
- Aprobacion multinivel configurable
- Notificaciones y escalados por cambio de estado
- Reapertura de demandas cerradas: se crea una nueva

## Decisions

**Maquina de estados explicita en una tabla, no condicionales dispersos.**
Una tabla de transiciones se lee de un vistazo y se contrasta con la spec linea
a linea. Con condicionales repartidos por el codigo, comprobar que la
implementacion coincide con el contrato exige leerlo entero.

**Una demanda asignada se cierra, no se cancela.**
Alternativa descartada: permitir cancelar en cualquier momento. Se descarto
porque deja asignaciones huerfanas que ningun proceso limpia, y porque en el
area la cancelacion tardia se resuelve hoy cerrando y abriendo otra.

## Risks / Trade-offs

Ocho estados es mucho para empezar y algunos podrian no usarse nunca. Se acepta
el riesgo porque salen del vocabulario que el area ya utiliza, y renombrar
estados mas adelante es mas caro que tener uno de mas.
