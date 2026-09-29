## Why

La capability `ocupacion-heredada` dejo por escrito que el calculo publicado
excluye el banquillo, promedia porcentajes redondeados, cuenta dias de
vacaciones como trabajados y no corta la sobreasignacion. El resultado agregado
es del 113,09% cuando el valor correcto es del 56,31%. Un numero por encima del
100% lleva anos publicandose sin que nadie lo recalculara.

## What Changes

Se corrigen los cuatro comportamientos, alineando el calculo heredado con la
capability `ocupacion`. Los requisitos que describian los defectos se MODIFICAN
para describir el comportamiento correcto.

## Capabilities

### New Capabilities

### Modified Capabilities
- `ocupacion-heredada`: los cuatro requisitos que describian defectos pasan a describir el comportamiento corregido

## Impact

El indicador de utilizacion del area que ve direccion baja 56,78 puntos. No es
un empeoramiento: es que se venia midiendo mal. Requiere aviso previo, recalculo
del historico y una nota explicativa en el primer cuadro de mando posterior al
despliegue.
