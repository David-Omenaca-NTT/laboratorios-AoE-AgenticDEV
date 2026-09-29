## Context

El catalogo de categorias y la politica de capacidad ya existen como ficheros
versionados por vigencia. El motor los consume, no los define.

## Goals / Non-Goals

**Goals:**
- Un veredicto reproducible y explicable, apto para justificarselo a la persona rechazada

**Non-Goals:**
- Ordenar o puntuar candidatos: eso es del agente, en otra capability
- Aprobacion multinivel de la sobreasignacion: aqui solo se consume el hecho

## Decisions

**El veredicto devuelve todos los motivos.**
Alternativa descartada: cortocircuitar al primer incumplimiento, que es mas
rapido. Se descarto porque produce explicaciones pobres: decirle a alguien que
no entro "por categoria" cuando ademas no tenia el nivel de skill obliga a
repetir la conversacion.

**El origen es un campo obligatorio y validado, no un texto libre.**
Un sistema que audita lo que hacen las personas y deja de auditar lo que hace un
agente no esta auditado. Que el origen sea obligatorio impide anadir una via
nueva sin declararla.

## Risks / Trade-offs

Comprobar el solape sobre el intervalo completo es mas caro que comparar fechas
de inicio. Con el volumen del area la diferencia es irrelevante y el error que
evita es de los que se detectan tarde y caros.
