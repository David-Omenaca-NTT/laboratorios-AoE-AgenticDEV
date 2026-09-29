# S8. Defensa ante panel

| | |
|---|---|
| Semana | 12 |
| Horas estimadas | 10 |
| Modulos del itinerario | 8 |

## Objetivo

Defender lo construido ante Head of AoE, SMEs y el dueno funcional de la herramienta.

## Por que esta estacion existe

Aqui el panel incluye a alguien que va a usar la herramienta de verdad. No es una simulacion: es aceptacion.

## Aviso

> La defensa del recorte es obligatoria. El PRD pedia 18 modulos, microservicios y Kafka. Tu has entregado 10 modulos parciales y un monolito modular. Si no sabes explicar por que eso es lo correcto, has construido algo que no sabes justificar.

## Que tienes que conseguir

1. Prepara 20 minutos con la estructura fija de la cohorte.
2. Incluye la defensa del recorte de alcance: por que este subconjunto del PRD y no otro, y por que un monolito modular y no microservicios.
3. Prepara la seccion de metricas: seguridad, utilidad, concentracion, MTTR y deteccion adversarial.
4. Prepara la decision de gobierno: por que tu agente se queda en N2.
5. Prepara una decision tecnica que tomaste y hoy tomarias distinta.

Esta guia dice que conseguir, no como. Si pudieras seguirla sin pensar, no
aprenderias nada que sirva cuando cambie el contexto, que es lo que pasa en
cliente el primer dia.

## Entregable

Demo, cuaderno de decisiones, metricas y defensa oral ante el dueno funcional.

## Como se cierra

```bash
abaco check S8 --prediccion pasa   # declara antes si crees que vas a pasar
abaco cerrar S8                    # sella la estacion y libera la referencia
```

Si te atascas: `abaco pista S8`. Si se agota la ventana,
`abaco desbloquear S8 --motivo "..."` te da la referencia como linea base y
te deja continuar. No penaliza las estaciones siguientes.

Criterios de superacion en CRITERIOS.md.
