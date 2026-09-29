# S4b. Flotilla multiagente

| | |
|---|---|
| Semana | 10 |
| Horas estimadas | 12 |
| Modulos del itinerario | 6 |

## Objetivo

Componer tres agentes sobre el mismo contexto y hacer explicito el contrato entre ellos.

## Por que esta estacion existe

Es la conversacion que se tiene en cliente cuando se pasa de un piloto a una flota.

## Aviso

> Los tres agentes no tienen el mismo techo. El de staffing propone personas y se queda en N2. El de conflictos no propone a nadie y puede llegar a N3. Justificar esa diferencia es el entregable intelectual de la estacion.

## Que tienes que conseguir

1. Trabajo de escuadra: componed staffing, deteccion de conflictos de asignacion y alerta de banquillo sobre el mismo servidor MCP.
2. Ejecutadlos en worktrees aislados y en paralelo.
3. Documentad el contrato: entradas, salidas, handoff y resolucion de conflicto.
4. Declarad el nivel de autonomia de cada uno y por que difieren.

Esta guia dice que conseguir, no como. Si pudieras seguirla sin pensar, no
aprenderias nada que sirva cuando cambie el contexto, que es lo que pasa en
cliente el primer dia.

## Entregable

Diagrama de flotilla, contrato validable contra esquema y grabacion de un ciclo completo.

## Como se cierra

```bash
abaco check S4b --prediccion pasa   # declara antes si crees que vas a pasar
abaco cerrar S4b                    # sella la estacion y libera la referencia
```

Si te atascas: `abaco pista S4b`. Si se agota la ventana,
`abaco desbloquear S4b --motivo "..."` te da la referencia como linea base y
te deja continuar. No penaliza las estaciones siguientes.

Criterios de superacion en CRITERIOS.md.
