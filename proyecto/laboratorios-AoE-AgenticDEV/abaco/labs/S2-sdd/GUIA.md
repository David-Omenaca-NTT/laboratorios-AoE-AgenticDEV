# S2. Spec-Driven Development

| | |
|---|---|
| Semana | 5 a 6 |
| Horas estimadas | 26 |
| Modulos del itinerario | 6 |

## Objetivo

Escribir SPEC-002 antes del codigo y derivar de ella la implementacion, con trazabilidad mecanica.

## Por que esta estacion existe

Es el posicionamiento de mercado del AoE. Escribir codigo con un agente lo hace cualquiera. Derivar codigo verificable de una especificacion trazable es lo que los clientes empiezan a pedir y casi nadie sabe hacer.

## Aviso

> La spec de partida contiene dos ambiguedades reales y deliberadas sobre el calculo de utilizacion. Si no las detectas, el agente producira una implementacion plausible y equivocada, y tu la aprobaras porque los tests que escribiste sobre tu suposicion pasaran. Detectarlas es criterio de evaluacion explicito.

## Que tienes que conseguir

1. Escribe SPEC-002 completa siguiendo la plantilla, antes de tocar codigo.
2. Numera los criterios y traducelos a test uno a uno, con la etiqueta `cubre:` en el docstring.
3. Dirige al agente para que derive la implementacion de la spec, criterio a criterio.
4. Detecta y resuelve las ambiguedades de la spec de partida ANTES de implementar.
5. Registra en el apartado de ambiguedades que estaba mal definido y como lo cerraste.

Esta guia dice que conseguir, no como. Si pudieras seguirla sin pensar, no
aprenderias nada que sirva cuando cambie el contexto, que es lo que pasa en
cliente el primer dia.

## Entregable

Spec versionada, implementacion completa, trazabilidad al 100% verificada por el pipeline y registro de ambiguedades.

## Como se cierra

```bash
abaco check S2 --prediccion pasa   # declara antes si crees que vas a pasar
abaco cerrar S2                    # sella la estacion y libera la referencia
```

Si te atascas: `abaco pista S2`. Si se agota la ventana,
`abaco desbloquear S2 --motivo "..."` te da la referencia como linea base y
te deja continuar. No penaliza las estaciones siguientes.

Criterios de superacion en CRITERIOS.md.
