# E6. El agente, especificado y generado

| | |
|---|---|
| Semana | 8 a 10 |
| Horas | 28 |

## Objetivo

Usar SDD para construir un agente que decide sobre personas.

## Que tienes que conseguir

1. Especifica el agente de propuesta de staffing, incluido su techo de autonomia.
2. Especifica la exigencia de alternativas descartadas y de evidencia por candidato.
3. Genera, mide seguridad, utilidad y concentracion.
4. Cuando la seguridad no llegue a cero, NO toques el agente: encuentra la restriccion que no habias especificado.

## Entregable

Agente generado con cero violaciones de restriccion dura, dos iteraciones medidas y la concentracion publicada.

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
abaco check E6 --prediccion pasa
abaco cerrar E6
```
