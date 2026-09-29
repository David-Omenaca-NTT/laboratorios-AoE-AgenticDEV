"""Servidor MCP del proyecto Aula.

Expone el contexto del repositorio como herramientas consultables por cualquier
agente. Implementa el transporte stdio de MCP con JSON-RPC 2.0 en biblioteca
estandar: sin SDK, para que el student vea el protocolo por dentro antes de
usar una abstraccion que se lo oculte.

Arranque:
    python3 -m agentes.mcp_aula.servidor

Registro en Claude Code (.mcp.json):
    {"mcpServers": {"abaco-contexto": {"command": "python3",
     "args": ["-m", "agentes.mcp_aula.servidor"]}}}
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
PROTOCOLO = "2024-11-05"

HERRAMIENTAS = [
    {
        "name": "listar_specs",
        "description": "Devuelve el catalogo de especificaciones del proyecto con su estado y version.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "obtener_spec",
        "description": "Devuelve una spec completa con sus criterios de aceptacion, invariantes y alcance.",
        "inputSchema": {
            "type": "object",
            "properties": {"id": {"type": "string", "description": "Identificador, por ejemplo SPEC-002"}},
            "required": ["id"],
        },
    },
    {
        "name": "trazabilidad",
        "description": "Para una spec, devuelve que criterios estan cubiertos por test y cuales no.",
        "inputSchema": {
            "type": "object",
            "properties": {"spec_id": {"type": "string"}},
            "required": ["spec_id"],
        },
    },
    {
        "name": "resultado_tests",
        "description": "Ejecuta la suite y devuelve el resultado agregado y los tests fallidos.",
        "inputSchema": {
            "type": "object",
            "properties": {"ruta": {"type": "string", "description": "Subconjunto opcional de tests"}},
            "required": [],
        },
    },
    {
        "name": "catalogo_vigente",
        "description": "Devuelve el catalogo de categorias profesionales vigente en una fecha, con su version y los parametros de cada categoria.",
        "inputSchema": {
            "type": "object",
            "properties": {"fecha": {"type": "string", "description": "ISO-8601, por defecto hoy"}},
            "required": [],
        },
    },
    {
        "name": "politica_vigente",
        "description": "Devuelve la politica de capacidad vigente: tolerancia de sobreasignacion y dedicaciones validas.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
]


# --- logica de las herramientas ----------------------------------------------

def _specs():
    return sorted((RAIZ / "specs").glob("SPEC-*.md"))


def _id_de(ruta: Path) -> str:
    return ruta.name.split("-")[0] + "-" + ruta.name.split("-")[1]


def _campo(texto: str, patron: str, defecto="desconocido") -> str:
    m = re.search(patron, texto, re.M)
    return m.group(1).strip() if m else defecto


def criterios_de(texto: str) -> list:
    """Extrae los identificadores CA-nn e INV-nn declarados en la spec."""
    return sorted(set(re.findall(r"\b(?:CA|INV)-\d{2}\b", texto)))


def listar_specs(_=None) -> dict:
    salida = []
    for ruta in _specs():
        texto = ruta.read_text(encoding="utf-8")
        salida.append({
            "id": _id_de(ruta),
            "titulo": _campo(texto, r"^#\s+SPEC-\d+:\s*(.+)$"),
            "version": _campo(texto, r"Versi[oó]n:\s*(v[\d.]+)"),
            "estado": _campo(texto, r"Estado:\s*(\w+)"),
            "criterios": len(criterios_de(texto)),
            "ruta": str(ruta.relative_to(RAIZ)),
        })
    return {"specs": salida}


def obtener_spec(args: dict) -> dict:
    ident = args["id"].upper()
    for ruta in _specs():
        if _id_de(ruta) == ident:
            texto = ruta.read_text(encoding="utf-8")
            return {"id": ident, "criterios": criterios_de(texto), "contenido": texto}
    return {"error": "spec %s no encontrada" % ident}


def _cubiertos() -> dict:
    """Mapea criterio -> lista de tests que lo declaran mediante `cubre:`."""
    mapa = {}
    for ruta in (RAIZ / "tests").rglob("test_*.py"):
        texto = ruta.read_text(encoding="utf-8")
        for bloque in re.finditer(r"def (test_\w+)\(.*?\):\s*(?:\"\"\"(.*?)\"\"\")?",
                                  texto, re.S):
            nombre, doc = bloque.group(1), bloque.group(2) or ""
            for etiqueta in re.findall(r"cubre:\s*([^\n\"]+)", doc):
                for ref in re.findall(r"(SPEC-\d+|LEG)[/-]((?:CA|INV|CAR|EQU)[-\w]*)", etiqueta):
                    clave = "%s/%s" % (ref[0], ref[1])
                    mapa.setdefault(clave, []).append("%s::%s" % (ruta.name, nombre))
    return mapa


def trazabilidad(args: dict) -> dict:
    ident = args["spec_id"].upper()
    spec = obtener_spec({"id": ident})
    if "error" in spec:
        return spec
    mapa = _cubiertos()
    cubiertos, huerfanos = {}, []
    for criterio in spec["criterios"]:
        clave = "%s/%s" % (ident, criterio)
        if clave in mapa:
            cubiertos[criterio] = mapa[clave]
        else:
            huerfanos.append(criterio)
    total = len(spec["criterios"])
    return {
        "spec": ident,
        "criterios_totales": total,
        "cubiertos": cubiertos,
        "sin_cubrir": huerfanos,
        "cobertura_pct": round(100.0 * (total - len(huerfanos)) / total, 1) if total else 0.0,
    }


def resultado_tests(args: dict) -> dict:
    ruta = args.get("ruta", "tests/")
    proc = subprocess.run([sys.executable, "-m", "pytest", ruta, "-q", "--no-header"],
                          cwd=RAIZ, capture_output=True, text=True)
    fallidos = re.findall(r"FAILED (\S+)", proc.stdout)
    resumen = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    return {"exito": proc.returncode == 0, "resumen": resumen, "fallidos": fallidos}


def catalogo_vigente(args: dict) -> dict:
    from datetime import date
    momento = date.fromisoformat(args["fecha"]) if args.get("fecha") else date.today()
    candidatos = []
    for fichero in sorted((RAIZ / "politicas" / "categorias").glob("*.json")):
        datos = json.loads(fichero.read_text(encoding="utf-8"))
        desde = date.fromisoformat(datos["vigente_desde"])
        if desde <= momento:
            candidatos.append((desde, datos))
    if not candidatos:
        return {"error": "no hay catalogo vigente en %s" % momento}
    datos = max(candidatos, key=lambda x: x[0])[1]
    return {
        "version": datos["version"], "vigente_desde": datos["vigente_desde"],
        "categorias": [
            {"codigo": c["codigo"], "nombre": c["nombre"],
             "orden_seniority": c["orden_seniority"],
             "utilizacion_objetivo": c["utilizacion_objetivo"]}
            for c in datos["categorias"]],
    }


def politica_vigente(args: dict) -> dict:
    ruta = RAIZ / "politicas" / "capacidad"
    ficheros = sorted(ruta.glob("*.json"))
    if not ficheros:
        return {"error": "no hay politica de capacidad"}
    return json.loads(ficheros[-1].read_text(encoding="utf-8"))


IMPLEMENTACION = {
    "listar_specs": listar_specs,
    "obtener_spec": obtener_spec,
    "trazabilidad": trazabilidad,
    "resultado_tests": resultado_tests,
    "catalogo_vigente": catalogo_vigente,
    "politica_vigente": politica_vigente,
}


# --- transporte JSON-RPC sobre stdio ------------------------------------------

def manejar(mensaje: dict):
    metodo = mensaje.get("method")
    ident = mensaje.get("id")

    if metodo == "initialize":
        return _ok(ident, {
            "protocolVersion": PROTOCOLO,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "abaco-contexto", "version": "1.0.0"},
        })
    if metodo == "tools/list":
        return _ok(ident, {"tools": HERRAMIENTAS})
    if metodo == "tools/call":
        nombre = mensaje["params"]["name"]
        args = mensaje["params"].get("arguments", {})
        if nombre not in IMPLEMENTACION:
            return _error(ident, -32601, "herramienta desconocida: %s" % nombre)
        try:
            resultado = IMPLEMENTACION[nombre](args)
        except Exception as exc:  # el agente debe recibir el fallo, no un cuelgue
            return _ok(ident, {"content": [{"type": "text", "text": "error: %s" % exc}],
                               "isError": True})
        return _ok(ident, {"content": [
            {"type": "text", "text": json.dumps(resultado, ensure_ascii=False, indent=2)}]})
    if metodo in ("notifications/initialized", "initialized"):
        return None
    return _error(ident, -32601, "metodo no soportado: %s" % metodo)


def _ok(ident, resultado):
    return {"jsonrpc": "2.0", "id": ident, "result": resultado}


def _error(ident, codigo, mensaje):
    return {"jsonrpc": "2.0", "id": ident, "error": {"code": codigo, "message": mensaje}}


def principal():
    for linea in sys.stdin:
        linea = linea.strip()
        if not linea:
            continue
        try:
            mensaje = json.loads(linea)
        except json.JSONDecodeError:
            continue
        respuesta = manejar(mensaje)
        if respuesta is not None:
            sys.stdout.write(json.dumps(respuesta, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    principal()
