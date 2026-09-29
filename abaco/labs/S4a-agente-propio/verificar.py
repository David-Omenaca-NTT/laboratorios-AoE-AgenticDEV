"""Verificador de S4a: Servidor MCP y agente de staffing."""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))

from abaco_cli.verificacion import (contiene, criterio, ejecutar, existe,
                                    orden_en_historial, prueba_negativa,
                                    pytest_verde)


import json


def verificar():
    c = []
    c.append(criterio("S4a-01", "el servidor MCP expone las seis herramientas",
                      all(contiene("agentes/mcp_abaco/servidor.py", h) for h in
                          ["listar_specs", "obtener_spec", "trazabilidad",
                           "resultado_tests", "catalogo_vigente", "politica_vigente"]),
                      "faltan herramientas en el servidor MCP"))

    p = ejecutar([sys.executable, "-c",
                  "import sys; sys.path.insert(0,'.');"
                  "from agentes.mcp_abaco.servidor import manejar;"
                  "r=manejar({'jsonrpc':'2.0','id':1,'method':'tools/list','params':{}});"
                  "print(len(r['result']['tools']))"])
    n = p.stdout.strip()
    c.append(criterio("S4a-02", "el servidor MCP responde a tools/list",
                      n.isdigit() and int(n) >= 6,
                      p.stderr.strip()[:200] or "herramientas: %s" % n))

    c.append(criterio("S4a-03", "el agente de staffing existe",
                      existe("agentes/staffing/agente.py"), "falta el agente"))

    c.append(criterio("S4a-04",
                      "la propuesta incluye las alternativas descartadas y su motivo",
                      contiene("agentes/staffing/agente.py", r"descartados")
                      and contiene("agentes/staffing/agente.py", r"class Descartado"),
                      "un agente que calla a quien descarto no es explicable"))

    p = ejecutar([sys.executable, "-m", "agentes.staffing.evaluar"])
    salida = p.stdout
    seguridad_ok = '"violaciones": 0' in salida
    c.append(criterio("S4a-05",
                      "SEGURIDAD: cero violaciones de restriccion dura",
                      seguridad_ok,
                      "toda violacion suspende la dimension, sin promediar con utilidad"))
    c.append(criterio("S4a-06", "UTILIDAD: la eleccion humana esta en el top 3",
                      '"supera": true' in salida.split('"utilidad"')[-1][:400]
                      if '"utilidad"' in salida else False,
                      "umbral 0,70"))

    informes = sorted((RAIZ / "evals" / "informes").glob("*.json")) \
        if (RAIZ / "evals" / "informes").exists() else []
    versiones = set()
    for i in informes:
        try:
            versiones.add(json.loads(i.read_text(encoding="utf-8")).get("version_agente"))
        except Exception:
            pass
    c.append(criterio("S4a-07",
                      "hay dos iteraciones medidas, linea base y version final",
                      len(versiones) >= 2,
                      "versiones encontradas: %s. Un agente que funciona a la primera no "
                      "ensena nada" % (sorted(v for v in versiones if v) or "ninguna")))

    c.append(criterio("S4a-08", "se mide la concentracion de propuestas",
                      contiene("agentes/staffing/evaluar.py", r"concentracion"),
                      "sin medir concentracion no se ve el sesgo del propio agente"))
    c.append(criterio("S4a-09", "el nucleo del agente es determinista",
                      contiene("agentes/staffing/agente.py", r"DETERMINISTA|determinista"),
                      "si el modelo decide a quien se propone, la decision no es defendible"))
    return c


if __name__ == "__main__":
    for x in verificar():
        print(("OK   " if x["ok"] else "FALLA"), x["id"], x["descripcion"], x["detalle"])
