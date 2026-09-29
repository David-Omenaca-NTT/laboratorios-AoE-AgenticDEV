## Why

El area necesita saber su ocupacion real. Hoy sale de una hoja heredada cuyo
numero nadie recalcula y que, al contrastarlo, da valores por encima del 100%.
De esa cifra cuelgan conversaciones de desempeno sobre personas concretas y el
cuadro de mando mensual de direccion, asi que el numero tiene que ser exacto y
reproducible.

## What Changes

Se introduce el calculo de utilizacion, sobreasignacion, cobertura de demanda y
deteccion de banquillo. Se resuelven de forma explicita las dos decisiones que
la peticion original dejaba abiertas: que entra en el denominador y que pasa con
una sobreasignacion.

## Capabilities

### New Capabilities
- `ocupacion`: calculo de utilizacion y ocupacion de personas y del area

### Modified Capabilities

## Impact

El numero de utilizacion del area cambia respecto del que se venia publicando.
La diferencia es de decenas de puntos y hay que anunciarla antes de sustituir la
fuente.
