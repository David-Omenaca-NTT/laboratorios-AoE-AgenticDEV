# S6. Gobierno de un agente que decide sobre personas

| | |
|---|---|
| Semana | 11 |
| Horas estimadas | 18 |
| Modulos del itinerario | 7 |

## Objetivo

Dejar el agente en condiciones de operar sobre datos reales de personas en una organizacion sujeta a normativa.

## Por que esta estacion existe

Es la estacion mas rica de los dos laboratorios. Un agente que propone quien trabaja en que afecta a carreras. La conversacion no es con un CTO: es con seguridad, con legal y con recursos humanos.

## Aviso

> El techo de autonomia no lo fija la precision del modelo, lo fija la reversibilidad del dano. Si llegas al panel defendiendo que tu agente podria ir en autonomo porque tiene buenas metricas, no has entendido la estacion, por muy buenas que sean tus metricas.

## Que tienes que conseguir

1. Escribe el Agent Release Manifest con los seis apartados adicionales: personas afectadas, explicabilidad, via de contestacion, veto humano, vigilancia de concentracion y datos excluidos.
2. Haz que el pipeline bloquee el merge si falta el manifiesto, si el hash no coincide, si la evaluacion caduco o si el nivel declarado supera N2.
3. Implementa el control que impide al agente leer los campos excluidos, y pruebalo intentando leerlos.
4. Mide la concentracion de tus propuestas y comenta el resultado.
5. Argumenta por escrito por que este agente NO debe llegar a N4, y que control haria falta para que otro agente si pudiera.
6. Calcula el coste en tokens por propuesta verificada.

Esta guia dice que conseguir, no como. Si pudieras seguirla sin pensar, no
aprenderias nada que sirva cuando cambie el contexto, que es lo que pasa en
cliente el primer dia.

## Entregable

Manifiestos validados por el pipeline, control de campos excluidos probado, informe de concentracion y argumentacion sobre N4.

## Como se cierra

```bash
abaco check S6 --prediccion pasa   # declara antes si crees que vas a pasar
abaco cerrar S6                    # sella la estacion y libera la referencia
```

Si te atascas: `abaco pista S6`. Si se agota la ventana,
`abaco desbloquear S6 --motivo "..."` te da la referencia como linea base y
te deja continuar. No penaliza las estaciones siguientes.

Criterios de superacion en CRITERIOS.md.
