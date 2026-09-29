## Why

El servicio se despliega sin forma de saber por que fallo ni de volver atras con
garantias. En el unico incidente de la fase de pruebas se tardo cuarenta y un
minutos en localizar una variable de entorno mal puesta.

## What Changes

Se anade observabilidad basica y un procedimiento de reversion ensayado, con el
objetivo de recuperacion declarado como requisito.

## Capabilities

### New Capabilities
- `operacion`: observabilidad y reversion del servicio desplegado

### Modified Capabilities

## Impact

Anade registro estructurado a las rutas de decision. Sin impacto sobre el
calculo ni sobre los datos.
