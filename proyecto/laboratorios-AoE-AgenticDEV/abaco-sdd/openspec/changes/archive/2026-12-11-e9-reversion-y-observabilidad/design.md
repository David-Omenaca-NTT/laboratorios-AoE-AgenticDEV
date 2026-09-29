## Context

El incidente de la fase de pruebas mostro el problema: el healthcheck seguia en
verde y solo fallaba el endpoint de evaluacion, lo que llevo a buscar en el
sitio equivocado durante veintidos minutos.

## Goals / Non-Goals

**Goals:**
- Que un fallo de configuracion se manifieste al arrancar y no al atender

**Non-Goals:**
- Trazado distribuido y metricas completas: fuera de alcance de la cohorte

## Decisions

**Fallar al arranque si la configuracion no resuelve.**
Alternativa descartada: degradar y seguir sirviendo. Se descarto porque un
servicio que arranca con la normativa equivocada produce decisiones equivocadas
en silencio, que es peor que no arrancar.

## Risks / Trade-offs

Fallar al arranque hace mas ruidoso un error de configuracion. Es exactamente lo
que se busca.
