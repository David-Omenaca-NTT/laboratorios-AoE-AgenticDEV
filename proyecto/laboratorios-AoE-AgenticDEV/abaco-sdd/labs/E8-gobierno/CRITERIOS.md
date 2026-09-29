# Criterios de superacion de E8

Lo que comprueba `abaco check E8`, ademas de las cuatro puertas y la
bateria de aceptacion.

## Entregable

Puertas activas y probadas con casos que deben fallar.

## Puertas que tienen que estar en verde

| Puerta | Que comprueba |
|--------|---------------|
| procedencia | Ningun commit sobre `src/` sin Change-Id valido |
| aceptacion | Ningun commit generado toca `aceptacion/` |
| deriva | Toda capability tiene modulo y todo modulo tiene capability |
| densidad | Escenarios por requisito dentro de rango |
