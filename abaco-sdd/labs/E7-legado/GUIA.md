# E7. Brownfield real

| | |
|---|---|
| Semana | 10 a 11 |
| Horas | 22 |

## Objetivo

Escribir la especificacion de lo que un sistema ya hace, antes de cambiarlo.

## Que tienes que conseguir

1. Escribe la capability que describe el comportamiento ACTUAL del modulo heredado, sin juzgarlo.
2. Bateria externa que confirma que tu descripcion coincide con la realidad.
3. Cambio aparte que MODIFICA esos requisitos con el comportamiento correcto.
4. Declara el impacto aguas abajo en la propuesta.

## Entregable

Dos cambios archivados: la caracterizacion y su correccion, con el impacto declarado.

## Recuerda la regla

> El codigo no se parchea. Se regenera. Si algo esta mal en el codigo,
> esta mal en la spec.

## Referencia de esta etapa

```bash
ls openspec/changes/archive/
```

Abre el cambio archivado de esta etapa y compara con el tuyo. La nota
didactica esta en su `LEEME.md`.

## Como se cierra

```bash
python3 -m herramientas.gates_sdd todos
python3 -m pytest aceptacion/ -q
openspec validate --all
abaco check E7 --prediccion pasa
abaco cerrar E7
```
