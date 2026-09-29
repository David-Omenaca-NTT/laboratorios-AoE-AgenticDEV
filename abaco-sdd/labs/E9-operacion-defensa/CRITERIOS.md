# Criterios de superacion de E9

Lo que comprueba `abaco check E9`, ademas de las cuatro puertas y la
bateria de aceptacion.

## Entregable

Servicio desplegado, MTTR de las dos rondas, y la defensa con el dato de cuanto cuesta la disciplina en un incidente.

## Puertas que tienen que estar en verde

| Puerta | Que comprueba |
|--------|---------------|
| procedencia | Ningun commit sobre `src/` sin Change-Id valido |
| aceptacion | Ningun commit generado toca `aceptacion/` |
| deriva | Toda capability tiene modulo y todo modulo tiene capability |
| densidad | Escenarios por requisito dentro de rango |
