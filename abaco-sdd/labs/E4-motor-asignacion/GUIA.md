# E4. Capability de reglas duras

| | |
|---|---|
| Semana | 5 a 6 |
| Horas | 26 |

## Objetivo

Especificar restricciones, no comportamientos vagos.

## Que tienes que conseguir

1. Especifica el motor de asignacion: capacidad, sobreasignacion, categoria, skill, disponibilidad.
2. Cada restriccion con su escenario de frontera.
3. Especifica la traza con campo origen, para que auditar al agente no sea opcional.
4. Ejercicio de arqueologia: te damos un modulo generado y localizas el requisito que lo origino.

## Entregable

Capability `asignacion` completa, bateria externa con los casos de frontera, ejercicio de arqueologia resuelto.

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
abaco check E4 --prediccion pasa
abaco cerrar E4
```
