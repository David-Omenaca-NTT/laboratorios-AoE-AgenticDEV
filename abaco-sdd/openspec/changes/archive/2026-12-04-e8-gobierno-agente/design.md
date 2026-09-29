## Context

El manifiesto ya existia como documento. Lo que no existia era ninguna
comprobacion automatica de que se cumpliera.

## Goals / Non-Goals

**Goals:**
- Que el gobierno falle solo cuando se incumple, sin depender de que alguien lo recuerde

**Non-Goals:**
- Sustituir la revision humana de las propuestas
- Auditar el contenido de las decisiones: eso lo hace la traza, no estas puertas

## Decisions

**El techo de autonomia se deduce de si el manifiesto declara personas afectadas.**
Alternativa descartada: una lista de agentes con su techo, mantenida a mano. Se
descarto porque se desactualiza en cuanto aparece un agente nuevo, y el fallo es
silencioso.

**La integridad de la bateria de aceptacion es un requisito de gobierno.**
Si el generador puede modificar el examen que lo evalua, no hay evaluacion. Es la
puerta que sostiene toda la modalidad.

## Risks / Trade-offs

Estas puertas van a bloquear merges legitimos al principio, sobre todo la de
procedencia. Es el coste de que la disciplina sea real y no declarativa.
