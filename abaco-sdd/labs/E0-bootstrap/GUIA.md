# E0. Bootstrap y contrato SDD

| | |
|---|---|
| Semana | 1 |
| Horas | 8 |

## Objetivo

Dejar el repositorio listo y entender por que aqui no se escribe implementacion.

## Que tienes que conseguir

1. Instala OpenSpec con la version fijada del repo y ejecuta `openspec init`.
2. Activa el perfil ampliado con `openspec config profile` y `openspec update`.
3. Desactiva la telemetria por politica y dejalo declarado en el contrato de contexto.
4. Rellena `openspec/config.yaml` con el contexto del proyecto y las reglas por artefacto.
5. Configura el pie de commit con Change-Id y Generated-By.
6. Firma el compromiso de datos personales.

## Entregable

Repositorio inicializado, telemetria desactivada, gates instalados y primer commit con procedencia.

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
abaco check E0 --prediccion pasa
abaco cerrar E0
```
