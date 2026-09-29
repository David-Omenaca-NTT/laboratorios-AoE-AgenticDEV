# S4a. Servidor MCP y agente de staffing

| | |
|---|---|
| Semana | 8 a 10 |
| Horas estimadas | 28 |
| Modulos del itinerario | 6 |

## Objetivo

Construir un agente que propone personas para una demanda, y medirlo con metricas separadas de seguridad y utilidad.

## Por que esta estacion existe

Es el corazon del laboratorio y la diferencia con Aula. Alli el agente revisaba codigo. Aqui propone personas, y una propuesta equivocada no es un bug: es la carrera de alguien.

## Aviso

> SEGURIDAD ES TOLERANCIA CERO. Proponer a alguien no disponible, por debajo de la categoria pedida o sin el nivel de skill exigido es una violacion, y una sola violacion en la entrega final suspende la dimension completa aunque tu utilidad sea perfecta. La seguridad no se promedia con nada.

## Que tienes que conseguir

1. Construye el servidor MCP con las seis herramientas del proyecto.
2. Construye el agente de staffing: recibe una demanda y propone candidatos ordenados con su evidencia.
3. Incluye siempre las alternativas descartadas y su motivo. Un agente que calla a quien descarto no es explicable.
4. Mide el agente v0 que trae el repo contra el conjunto de evaluacion y guarda el informe.
5. Itera hasta cero violaciones de restriccion dura y utilidad por encima de 0,70, y guarda el segundo informe.
6. Mide la concentracion: cuantas personas distintas propone tu agente sobre el pool.
7. Explica por escrito que cambiaste entre las dos versiones y por que mejoro.

Esta guia dice que conseguir, no como. Si pudieras seguirla sin pensar, no
aprenderias nada que sirva cuando cambie el contexto, que es lo que pasa en
cliente el primer dia.

## Entregable

Servidor MCP funcionando, agente con propuesta explicable, informe con las dos iteraciones y las tres metricas.

## Como se cierra

```bash
abaco check S4a --prediccion pasa   # declara antes si crees que vas a pasar
abaco cerrar S4a                    # sella la estacion y libera la referencia
```

Si te atascas: `abaco pista S4a`. Si se agota la ventana,
`abaco desbloquear S4a --motivo "..."` te da la referencia como linea base y
te deja continuar. No penaliza las estaciones siguientes.

Criterios de superacion en CRITERIOS.md.
