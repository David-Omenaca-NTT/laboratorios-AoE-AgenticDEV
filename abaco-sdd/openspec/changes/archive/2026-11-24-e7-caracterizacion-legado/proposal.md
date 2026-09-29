## Why

El calculo de utilizacion que publica el cuadro de mando sale de un modulo
heredado sin tests ni documentacion, con parches acumulados desde 2019. Antes de
sustituirlo hay que saber exactamente que hace, incluido lo que hace mal.

## What Changes

Se anade una capability que describe el comportamiento ACTUAL del modulo
heredado. Describe defectos como si fueran reglas, a proposito: primero se fija
la realidad y despues se corrige, en un cambio aparte, para que quede por escrito
que se cambio y por que.

## Capabilities

### New Capabilities
- `ocupacion-heredada`: comportamiento observado del calculo de utilizacion heredado, incluidos sus defectos

### Modified Capabilities

## Impact

No modifica ningun comportamiento. Es una descripcion. El unico impacto es que a
partir de aqui existe una red de seguridad para tocar el modulo.
