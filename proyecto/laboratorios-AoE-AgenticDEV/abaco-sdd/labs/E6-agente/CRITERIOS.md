# Criterios de superacion de E6

Lo que comprueba `abaco check E6`, ademas de las cuatro puertas y la
bateria de aceptacion.

## Entregable

Agente generado con cero violaciones de restriccion dura, dos iteraciones medidas y la concentracion publicada.

## Puertas que tienen que estar en verde

| Puerta | Que comprueba |
|--------|---------------|
| procedencia | Ningun commit sobre `src/` sin Change-Id valido |
| aceptacion | Ningun commit generado toca `aceptacion/` |
| deriva | Toda capability tiene modulo y todo modulo tiene capability |
| densidad | Escenarios por requisito dentro de rango |
