# E9. Despliegue, deriva y defensa

| | |
|---|---|
| Semana | 12 |
| Horas | 24 |

## Objetivo

Corregir produccion por especificacion, y defender la modalidad entera.

## Que tienes que conseguir

1. Especifica observabilidad y reversion con objetivo de tiempo.
2. Fallo inducido cruzado: dos rondas, con y sin agente de triaje.
3. IMPORTANTE: la correccion del fallo tambien pasa por especificacion. Mide cuanto cuesta.
4. Prepara la defensa: coste real de la modalidad y en que contextos la recomendarias.

## Entregable

Servicio desplegado, MTTR de las dos rondas, y la defensa con el dato de cuanto cuesta la disciplina en un incidente.

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
abaco check E9 --prediccion pasa
abaco cerrar E9
```
