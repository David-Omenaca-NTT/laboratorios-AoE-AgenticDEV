# E1. El ciclo completo en pequeno

| | |
|---|---|
| Semana | 2 |
| Horas | 16 |

## Objetivo

Recorrer el ciclo entero una vez sobre algo trivial, antes de que el dominio distraiga.

## Que tienes que conseguir

1. Ejecuta `/opsx:onboard` para ver el ciclo narrado sobre el codigo real.
2. Propon tu primer cambio propio: la comprobacion de salud del servicio.
3. Revisa los cuatro artefactos ANTES de aplicar. Si la propuesta esta mal, todo lo demas hereda el error.
4. Aplica, verifica y archiva.
5. Comprueba que la especificacion principal quedo actualizada.

## Entregable

Un cambio archivado con sus cuatro artefactos y la capability creada en `openspec/specs/`.

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
abaco check E1 --prediccion pasa
abaco cerrar E1
```
