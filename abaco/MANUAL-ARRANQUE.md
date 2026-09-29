# Manual de arranque — Ábaco

## Requisitos

- Python 3.11.
- Dependencias: `python3 -m pip install -r requirements.txt`.

## Preparación

Desde la carpeta `abaco`:

```bash
python3 herramientas/generar_corpus.py
python3 -m pytest tests/ -q
```

El corpus generado es sintético y determinista. No incorpores datos personales reales.

## Arranque local

```bash
PYTHONPATH=src uvicorn abaco.api.app:app --host 127.0.0.1 --port 8002
```

El servicio queda expuesto únicamente en `http://127.0.0.1:8002`.

## Comprobación

```bash
python3 -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8002/salud').read().decode())"
```

La respuesta debe contener `"estado": "ok"`.

## Recursos HTTP

- `GET /salud`
- `POST /demandas`
- `POST /demandas/{demanda_id}/transicion`
- `GET /demandas/{demanda_id}`

La documentación interactiva está disponible en `http://127.0.0.1:8002/docs`.

## Detención

Pulsa `Ctrl+C` en la terminal de Uvicorn.
