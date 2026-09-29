# S1. Rebanada vertical a mano

| | |
|---|---|
| Semana | 2 a 4 |
| Horas estimadas | 24 |
| Modulos del itinerario | 2, 3, 4 |

## Objetivo

Construir el alta de demanda y su maquina de estados completa, sin ningun agente.

## Por que esta estacion existe

No se puede revisar lo que no se sabe escribir. Si llegas al modulo 5 sin haber escrito un test a mano, aceptaras lo que te proponga el agente porque no tendras criterio con el que discrepar. Ademas, el tiempo que registres aqui es tu linea base para medir tu propio salto en S2 y S3.

## Que tienes que conseguir

1. Implementa la maquina de estados de la demanda con sus ocho estados y las transiciones validas.
2. Implementa el alta de demanda: endpoint, validacion, persistencia en memoria y tests.
3. Escribe los tests a mano, incluidos los casos limite de transicion invalida.
4. Contenedoriza el servicio con una imagen OCI multi-stage.
5. Monta el pipeline: build, test, cobertura y publicacion de imagen.
6. Registra el tiempo por tarea en bitacora.md.

Esta guia dice que conseguir, no como. Si pudieras seguirla sin pensar, no
aprenderias nada que sirva cuando cambie el contexto, que es lo que pasa en
cliente el primer dia.

## Entregable

Pipeline verde de extremo a extremo, imagen publicada, maquina de estados completa con tests.

## Como se cierra

```bash
abaco check S1 --prediccion pasa   # declara antes si crees que vas a pasar
abaco cerrar S1                    # sella la estacion y libera la referencia
```

Si te atascas: `abaco pista S1`. Si se agota la ventana,
`abaco desbloquear S1 --motivo "..."` te da la referencia como linea base y
te deja continuar. No penaliza las estaciones siguientes.

Criterios de superacion en CRITERIOS.md.
