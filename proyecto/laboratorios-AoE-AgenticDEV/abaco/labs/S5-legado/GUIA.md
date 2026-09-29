# S5. Modernizacion del legado con agentes

| | |
|---|---|
| Semana | 10 a 11 |
| Horas estimadas | 22 |
| Modulos del itinerario | 5, 6 |

## Objetivo

Caracterizar, refactorizar y demostrar equivalencia sobre la calculadora de utilizacion heredada.

## Por que esta estacion existe

Es el escenario mas frecuente en cliente real. Y aqui el numero heredado alimenta el cuadro de mando que ve direccion, asi que corregirlo tiene consecuencias que hay que anunciar antes, no despues.

## Aviso

> REGLA DURA: esta prohibido pedir al agente que refactorice antes de que exista la caracterizacion. El verificador comprueba el orden en el historial de git. Suspende la estacion. Es tambien la falta que veras cometer en cliente.

## Que tienes que conseguir

1. Escribe la bateria de caracterizacion que captura el comportamiento actual, incluidos los comportamientos no documentados.
2. Commitea la caracterizacion ANTES de tocar una linea del legado.
3. Refactoriza con la red puesta, con la bateria en verde en cada paso.
4. Ejecuta la equivalencia sobre el corpus completo.
5. Declara cada desviacion en DESVIACIONES.md con categoria, causa y efecto aguas abajo.

Esta guia dice que conseguir, no como. Si pudieras seguirla sin pensar, no
aprenderias nada que sirva cuando cambie el contexto, que es lo que pasa en
cliente el primer dia.

## Entregable

Caracterizacion completa, refactor entregado, informe de equivalencia sin desviaciones sin justificar.

## Como se cierra

```bash
abaco check S5 --prediccion pasa   # declara antes si crees que vas a pasar
abaco cerrar S5                    # sella la estacion y libera la referencia
```

Si te atascas: `abaco pista S5`. Si se agota la ventana,
`abaco desbloquear S5 --motivo "..."` te da la referencia como linea base y
te deja continuar. No penaliza las estaciones siguientes.

Criterios de superacion en CRITERIOS.md.
