# Criterios de superacion de E7

Lo que comprueba `abaco check E7`, ademas de las cuatro puertas y la
bateria de aceptacion.

## Entregable

Dos cambios archivados: la caracterizacion y su correccion, con el impacto declarado.

## Puertas que tienen que estar en verde

| Puerta | Que comprueba |
|--------|---------------|
| procedencia | Ningun commit sobre `src/` sin Change-Id valido |
| aceptacion | Ningun commit generado toca `aceptacion/` |
| deriva | Toda capability tiene modulo y todo modulo tiene capability |
| densidad | Escenarios por requisito dentro de rango |
