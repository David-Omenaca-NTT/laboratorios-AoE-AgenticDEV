# Criterios de superacion de E2

Lo que comprueba `abaco check E2`, ademas de las cuatro puertas y la
bateria de aceptacion.

## Entregable

Capability `demanda` completa, con la bateria externa cubriendo todos sus escenarios.

## Puertas que tienen que estar en verde

| Puerta | Que comprueba |
|--------|---------------|
| procedencia | Ningun commit sobre `src/` sin Change-Id valido |
| aceptacion | Ningun commit generado toca `aceptacion/` |
| deriva | Toda capability tiene modulo y todo modulo tiene capability |
| densidad | Escenarios por requisito dentro de rango |
