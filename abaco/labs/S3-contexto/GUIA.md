# S3. Ingenieria de contexto y operacion de agentes

| | |
|---|---|
| Semana | 6 a 7 |
| Horas estimadas | 24 |
| Modulos del itinerario | 5 |

## Objetivo

Convertir el repositorio en un entorno donde el agente trabaja bien por diseno, no por suerte en el prompt.

## Por que esta estacion existe

Lo innegociable no se pide en lenguaje natural, se hace determinista. En este proyecto ademas hay una linea que ningun agente puede cruzar: los datos personales. Eso no se confia a una instruccion.

## Aviso

> Se mide tu ratio de diff aceptado sin comentario. Un ratio alto no es productividad, es aceptacion ciega. Un ratio de cero tampoco es bueno.

## Que tienes que conseguir

1. Escribe CLAUDE.md con las seis secciones obligatorias.
2. Declara en la seccion de limites los campos de perfil que ningun agente puede leer.
3. Configura allowlist y hooks: formato, bloqueo de rutas prohibidas, tests antes de commit.
4. Define dos subagentes acotados: uno implementa, otro revisa solo el diff.
5. Resuelve el mismo encargo con Claude Code y con OpenCode y entrega la comparativa razonada.
6. Ejecuta un ciclo en worktrees paralelos con Orca, patron escritor y revisor.

Esta guia dice que conseguir, no como. Si pudieras seguirla sin pensar, no
aprenderias nada que sirva cuando cambie el contexto, que es lo que pasa en
cliente el primer dia.

## Entregable

Configuracion versionada, cuatro PRs generados con agente y revisados con evidencia, tabla comparativa entregada.

## Como se cierra

```bash
abaco check S3 --prediccion pasa   # declara antes si crees que vas a pasar
abaco cerrar S3                    # sella la estacion y libera la referencia
```

Si te atascas: `abaco pista S3`. Si se agota la ventana,
`abaco desbloquear S3 --motivo "..."` te da la referencia como linea base y
te deja continuar. No penaliza las estaciones siguientes.

Criterios de superacion en CRITERIOS.md.
