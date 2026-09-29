## Why

El servicio no expone ninguna forma de saber si esta vivo. El pipeline de
despliegue necesita un punto de comprobacion antes de dar por buena una
version, y la reversion automatica necesita saber contra que preguntar.

## What Changes

Se anade un endpoint de comprobacion de salud que responde el estado del
servicio y la version del catalogo de categorias cargado.

## Capabilities

### New Capabilities
- `salud`: comprobacion de disponibilidad del servicio y de la configuracion cargada

### Modified Capabilities

## Impact

Nuevo endpoint publico sin autenticacion. Sin impacto en datos.
