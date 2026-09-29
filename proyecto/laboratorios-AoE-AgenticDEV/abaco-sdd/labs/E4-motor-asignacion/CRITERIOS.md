# Criterios de superacion de E4

Lo que comprueba `abaco check E4`, ademas de las cuatro puertas y la
bateria de aceptacion.

## Entregable

Capability `asignacion` completa, bateria externa con los casos de frontera, ejercicio de arqueologia resuelto.

## Puertas que tienen que estar en verde

| Puerta | Que comprueba |
|--------|---------------|
| procedencia | Ningun commit sobre `src/` sin Change-Id valido |
| aceptacion | Ningun commit generado toca `aceptacion/` |
| deriva | Toda capability tiene modulo y todo modulo tiene capability |
| densidad | Escenarios por requisito dentro de rango |
