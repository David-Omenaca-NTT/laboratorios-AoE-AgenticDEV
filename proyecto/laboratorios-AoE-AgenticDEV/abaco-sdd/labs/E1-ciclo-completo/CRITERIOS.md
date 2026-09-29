# Criterios de superacion de E1

Lo que comprueba `abaco check E1`, ademas de las cuatro puertas y la
bateria de aceptacion.

## Entregable

Un cambio archivado con sus cuatro artefactos y la capability creada en `openspec/specs/`.

## Puertas que tienen que estar en verde

| Puerta | Que comprueba |
|--------|---------------|
| procedencia | Ningun commit sobre `src/` sin Change-Id valido |
| aceptacion | Ningun commit generado toca `aceptacion/` |
| deriva | Toda capability tiene modulo y todo modulo tiene capability |
| densidad | Escenarios por requisito dentro de rango |
