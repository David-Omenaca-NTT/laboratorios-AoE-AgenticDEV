# E8. Gobierno de especificaciones y de agentes

| | |
|---|---|
| Semana | 11 |
| Horas | 18 |

## Objetivo

Convertir el gobierno en puertas que fallan solas.

## Que tienes que conseguir

1. Especifica el gobierno como requisitos verificables, no como politica escrita.
2. Manifiesto obligatorio con los apartados sobre personas afectadas y contestacion.
3. Techo de autonomia deducido de si el manifiesto declara personas afectadas.
4. Prueba las puertas rompiendolas a proposito.

## Entregable

Puertas activas y probadas con casos que deben fallar.

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
abaco check E8 --prediccion pasa
abaco cerrar E8
```
