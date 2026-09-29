# E5. Capability numerica y la ambiguedad

| | |
|---|---|
| Semana | 6 a 7 |
| Horas | 26 |

## Objetivo

Descubrir que SDD no protege de una especificacion equivocada.

## Que tienes que conseguir

1. Especifica el calculo de utilizacion, sobreasignacion, cobertura y banquillo.
2. Genera y comprueba contra la bateria externa.
3. Cuando algo no cuadre, encuentra que decision no habias tomado.
4. Registra la ambiguedad y la alternativa descartada en el diseno.

## Entregable

Capability `ocupacion` completa, con las ambiguedades resueltas y documentadas.

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
abaco check E5 --prediccion pasa
abaco cerrar E5
```
