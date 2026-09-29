# E2. Primera capability: ciclo de vida de la demanda

| | |
|---|---|
| Semana | 2 a 3 |
| Horas | 20 |

## Objetivo

Escribir requisitos y escenarios que generan codigo correcto a la primera.

## Que tienes que conseguir

1. Especifica los ocho estados de la demanda y sus transiciones validas.
2. Escribe al menos un escenario negativo por requisito.
3. Genera y comprueba contra tu bateria de aceptacion externa.
4. Escribe la bateria a mano en `aceptacion/`. Ningun agente entra ahi.

## Entregable

Capability `demanda` completa, con la bateria externa cubriendo todos sus escenarios.

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
abaco check E2 --prediccion pasa
abaco cerrar E2
```
