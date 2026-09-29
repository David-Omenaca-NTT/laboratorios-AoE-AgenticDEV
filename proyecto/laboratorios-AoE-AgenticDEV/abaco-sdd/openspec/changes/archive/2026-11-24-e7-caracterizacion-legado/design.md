## Context

El modulo tiene unas trescientas lineas, numeros magicos, codigo muerto y cuatro
parches sin ticket. Nadie del equipo actual lo escribio.

## Goals / Non-Goals

**Goals:**
- Fijar la realidad antes de tocarla

**Non-Goals:**
- Corregir nada. Eso es el cambio siguiente, a proposito

## Decisions

**Los requisitos describen defectos como si fueran reglas.**
Es incomodo y es deliberado. Un requisito que dice "el calculo excluye el
banquillo" no esta aprobando ese comportamiento: esta constatandolo. La
correccion llega en el cambio siguiente y asi el archivo conserva las dos
versiones y la fecha en que se paso de una a otra.

**La caracterizacion precede al refactor, y el orden se comprueba.**
Alternativa descartada: refactorizar y escribir tests despues. Se descarto
porque entonces los tests describen el codigo nuevo y no hay forma de saber si
se rompio algo por el camino.

## Risks / Trade-offs

Quien lea esta capability sin contexto puede pensar que estos comportamientos
son deseados. El proposito de la capability lo advierte, y el cambio siguiente
los modifica pocos dias despues.
