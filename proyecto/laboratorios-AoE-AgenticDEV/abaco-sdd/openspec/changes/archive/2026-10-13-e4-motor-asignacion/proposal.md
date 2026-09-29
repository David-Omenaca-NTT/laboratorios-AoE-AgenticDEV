## Why

Decidir si alguien puede entrar en una posicion se hace hoy de cabeza, mirando
un calendario compartido. Se cometen dos errores recurrentes: asignar a alguien
que ya esta al 100% y asignar por debajo de la categoria pedida. El primero se
detecta tarde y el segundo casi nunca.

## What Changes

Se introduce el motor de asignacion: dado un candidato, una posicion y un
periodo, decide si es apto y devuelve todos los motivos por los que no lo es.

## Capabilities

### New Capabilities
- `asignacion`: reglas duras que deciden si una persona puede ocupar una posicion en un periodo

### Modified Capabilities

## Impact

Nueva capability. Consume el catalogo de categorias y la politica de capacidad,
ambos versionados. No modifica la capability de demanda.
