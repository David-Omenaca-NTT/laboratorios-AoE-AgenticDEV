## Context

El requisito original prohibia esta transicion a proposito, por el problema de
las asignaciones huerfanas. El caso de negocio que aparece ahora es real y no se
puede resolver cerrando la demanda, porque falsea la cobertura.

## Goals / Non-Goals

**Goals:**
- Permitir el caso real sin perder el motivo por el que estaba prohibido

**Non-Goals:**
- Cancelar en cascada las asignaciones vinculadas: eso es otra decision y otro cambio

## Decisions

**Se MODIFICA el requisito, no se elimina y se crea otro.**
Asi el histrorico del archivo conserva por que estaba prohibido y por que se
levanto la prohibicion. Si se borra y se escribe uno nuevo, dentro de un ano
nadie sabra que hubo una razon.

**El motivo es obligatorio y la constancia es automatica.**
Alternativa descartada: permitir la cancelacion sin mas. Se descarto porque el
riesgo que motivaba la prohibicion sigue existiendo: lo unico que cambia es que
ahora queda registrado quien asumio ese riesgo y por que.

## Risks / Trade-offs

La cobertura del area baja al desplegar esto, y va a parecer un empeoramiento
cuando en realidad es que antes se estaba midiendo mal. Hay que anunciarlo.
