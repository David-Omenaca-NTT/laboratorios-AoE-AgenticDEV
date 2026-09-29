## Why

Hoy una demanda de recursos vive en un correo y en la cabeza de quien la pidio.
No hay forma de saber si una peticion esta pendiente de aprobar, buscando
candidato o ya cerrada, y eso hace imposible medir cuanto tarda el area en
cubrir una posicion.

## What Changes

Se introduce el ciclo de vida de la demanda con sus ocho estados y las
transiciones permitidas entre ellos. Una demanda en estado terminal deja de
admitir asignaciones.

## Capabilities

### New Capabilities
- `demanda`: ciclo de vida de una peticion de recursos, desde que se solicita hasta que se cierra o se cancela

### Modified Capabilities

## Impact

Nueva capability. Sin impacto sobre datos existentes: no hay demandas previas
que migrar.
