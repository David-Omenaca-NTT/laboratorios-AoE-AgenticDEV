## Context

La peticion original dejaba dos decisiones abiertas y no lo decia. Cualquiera de
las dos lecturas produce un sistema que funciona, pasa sus tests y da numeros
distintos. Se resuelven aqui de forma explicita, con la alternativa descartada
por escrito, porque dentro de un ano alguien va a preguntar por que.

## Goals / Non-Goals

**Goals:**
- Un numero exacto, reproducible y defendible ante la persona a la que se le mide

**Non-Goals:**
- Coste, tarifa y margen: fuera del sistema por minimizacion de datos
- Imputacion real de horas: se calcula sobre asignacion, no sobre parte de horas

## Decisions

**Decision 1: la formacion y el banquillo entran en el denominador.**
Alternativa descartada: excluirlos, que es lo que hace el sistema heredado. Se
descarto porque sube la utilizacion del area sin que nadie haya trabajado mas.
Un area con una persona ocupada y cuatro paradas no esta al 100%.

**Decision 2: la sobreasignacion se corta en el 100% y se reporta aparte.**
Alternativa descartada: dejar que una persona al 120% aporte 120. Se descarto
porque hace que un equipo quemado parezca un equipo eficiente y esconde
exactamente lo que hay que vigilar.

**Decision 3: se agrega y luego se redondea, una sola vez.**
Alternativa descartada: promediar porcentajes individuales. Se descarto porque
da el mismo peso a alguien con dos dias de capacidad que a alguien con veinte.

## Risks / Trade-offs

Las tres decisiones bajan el numero publicado. Va a parecer un empeoramiento
cuando lo que ocurre es que antes se medi­a mal. El riesgo real no es tecnico:
es de comunicacion, y se mitiga anunciandolo antes con el detalle que lo compone.
