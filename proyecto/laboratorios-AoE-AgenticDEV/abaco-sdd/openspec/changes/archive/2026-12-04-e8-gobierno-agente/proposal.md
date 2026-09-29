## Why

El agente de staffing ya funciona y propone sobre datos de personas reales. No
hay hoy ninguna forma mecanica de comprobar que sigue dentro de su techo de
autonomia, ni de saber quien puede impugnar una propuesta, ni de detectar que el
codigo se ha ido de lo que dice su especificacion.

## What Changes

Se introduce el gobierno del agente como requisitos verificables: manifiesto
obligatorio con apartados de personas afectadas y contestacion, techo de
autonomia comprobado en el pipeline, y medicion de la deriva entre
especificacion y codigo.

## Capabilities

### New Capabilities
- `gobierno-agentes`: control mecanico del ciclo de vida de un agente que decide sobre personas

### Modified Capabilities

## Impact

Anade puertas al pipeline que pueden bloquear merges. Es intencionado: un
gobierno que solo avisa no es un gobierno.
