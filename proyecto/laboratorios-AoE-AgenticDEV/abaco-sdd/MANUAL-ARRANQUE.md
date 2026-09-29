# Manual de arranque — Ábaco-SDD

## Requisitos

- Python 3.11.
- Dependencias instaladas: `python3 -m pip install -r requirements.txt`.
- OpenSpec 1.8.0 si se desea validar las especificaciones:

  ```bash
  npm install -g @fission-ai/openspec@1.8.0
  export OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1
  ```

## Preparación

Desde la carpeta `abaco-sdd`:

```bash
python3 herramientas/generar_corpus.py
python3 -m pytest aceptacion/ -q
```

El corpus es sintético y determinista; no incorpores datos personales reales.

## Arranque local

```bash
PYTHONPATH=src uvicorn abaco.api.app:app --host 127.0.0.1 --port 8000
```

El servicio queda disponible únicamente en local en `http://127.0.0.1:8000`.

## Comprobación de salud

En otra terminal:

```bash
python3 -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/salud').read().decode())"
```

La respuesta esperada contiene `"estado": "ok"`.

## Endpoints disponibles

- `GET /salud`
- `POST /demandas`
- `POST /demandas/{demanda_id}/transicion`
- `GET /demandas/{demanda_id}`

La documentación interactiva de FastAPI está en `http://127.0.0.1:8000/docs` mientras el servicio está activo.

## Detención

Usa `Ctrl+C` en la terminal que ejecuta Uvicorn.

## Validación SDD opcional

```bash
openspec validate --all
python3 -m herramientas.gates_sdd todos
```
