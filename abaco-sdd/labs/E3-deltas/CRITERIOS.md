# Criterios de superacion de E3

Lo que comprueba `abaco check E3`, ademas de las cuatro puertas y la
bateria de aceptacion.

## Entregable

Delta aplicado, spec principal fusionada sin perdida de escenarios, cambio archivado.

## Puertas que tienen que estar en verde

| Puerta | Que comprueba |
|--------|---------------|
| procedencia | Ningun commit sobre `src/` sin Change-Id valido |
| aceptacion | Ningun commit generado toca `aceptacion/` |
| deriva | Toda capability tiene modulo y todo modulo tiene capability |
| densidad | Escenarios por requisito dentro de rango |
