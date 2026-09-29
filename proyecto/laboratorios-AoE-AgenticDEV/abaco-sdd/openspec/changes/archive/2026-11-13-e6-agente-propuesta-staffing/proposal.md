## Why

Cubrir una demanda exige hoy que una persona revise a mano quien tiene el skill,
quien esta libre y quien encaja en categoria. Sobre un pool de ciento ochenta
personas eso lleva unos veinte minutos por posicion y se hace mirando siempre a
los mismos, porque son los que uno recuerda.

## What Changes

Se introduce un agente que propone candidatos ordenados para cada posicion de
una demanda, con la evidencia de por que entra cada uno y por que queda fuera
cada descartado. El agente propone; decide siempre una persona.

## Capabilities

### New Capabilities
- `agente-staffing`: propuesta explicable de candidatos para una demanda, con techo de autonomia declarado

### Modified Capabilities

## Impact

El agente lee categoria, skills, asignaciones y ausencias. NO lee nombre, correo,
telefono, pais, oficina ni ningun dato de identificacion personal. No crea
asignaciones en ningun caso.
