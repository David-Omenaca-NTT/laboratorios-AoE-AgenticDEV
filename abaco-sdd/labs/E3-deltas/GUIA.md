# E3. Deltas sobre lo existente

| | |
|---|---|
| Semana | 4 |
| Horas | 18 |

## Objetivo

Modificar una capability sin reescribirla. Es lo que se hace en cliente.

## Que tienes que conseguir

1. Recibe un cambio normativo: una demanda asignada pasa a poder cancelarse bajo condicion.
2. Exprésalo como delta con MODIFIED y ADDED, no reescribiendo la capability.
3. Sincroniza y comprueba que se fusiono lo que esperabas y no se perdio nada.
4. Archiva.

## Entregable

Delta aplicado, spec principal fusionada sin perdida de escenarios, cambio archivado.

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
abaco check E3 --prediccion pasa
abaco cerrar E3
```
