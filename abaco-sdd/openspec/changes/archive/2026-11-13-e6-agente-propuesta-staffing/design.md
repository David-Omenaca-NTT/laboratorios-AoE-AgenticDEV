## Context

Existe ya la capability de asignacion con las restricciones duras. El agente no
las reimplementa: las consume. Si lo hiciera por su cuenta habria dos verdades y
una acabaria desviandose.

## Goals / Non-Goals

**Goals:**
- Una propuesta que se pueda defender ante la persona que no fue propuesta

**Non-Goals:**
- Decidir. El agente propone
- Optimizar el reparto del trabajo entre personas: se mide la concentracion, no se corrige sola

## Decisions

**El nucleo es determinista y el modelo solo redacta.**
Alternativa descartada: dejar que el modelo ordene y decida. Se descarto por dos
motivos: un resultado que cambia entre ejecuciones no sirve como base de una
decision sobre una persona, y no se puede auditar.

**El techo de autonomia es un requisito con escenario, no una nota de diseno.**
Si estuviera solo en la documentacion, el generador podria producir una via de
escritura sin infringir nada. Como escenario, es verificable.

**Se mide la concentracion aunque no haya umbral.**
Optimizar por encaje concentra el trabajo en las mismas personas. No se corrige
automaticamente porque eso seria meter un criterio de reparto dentro de una
decision que corresponde a un humano. Se mide, se publica y decide el resource
manager.

## Risks / Trade-offs

Un agente mas seguro y mas util tiende a ser mas concentrado. Es un efecto
esperado y esta declarado: sin medirlo, el agente parece perfecto.
