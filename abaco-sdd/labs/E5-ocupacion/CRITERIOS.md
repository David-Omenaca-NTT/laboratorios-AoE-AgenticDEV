# Criterios de superacion de E5

Lo que comprueba `abaco check E5`, ademas de las cuatro puertas y la
bateria de aceptacion.

## Entregable

Capability `ocupacion` completa, con las ambiguedades resueltas y documentadas.

## Puertas que tienen que estar en verde

| Puerta | Que comprueba |
|--------|---------------|
| procedencia | Ningun commit sobre `src/` sin Change-Id valido |
| aceptacion | Ningun commit generado toca `aceptacion/` |
| deriva | Toda capability tiene modulo y todo modulo tiene capability |
| densidad | Escenarios por requisito dentro de rango |
