"""Verificador de S2: Spec-Driven Development."""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))

from abaco_cli.verificacion import (contiene, criterio, ejecutar, existe,
                                    orden_en_historial, prueba_negativa,
                                    pytest_verde)


from agentes.mcp_abaco.servidor import listar_specs, trazabilidad
from abaco_cli.verificacion import mutar_y_exigir_fallo


def verificar():
    c = []
    specs = listar_specs()["specs"]
    activas = [s for s in specs if s["estado"] == "activa"]
    c.append(criterio("S2-01", "existen specs activas", bool(activas),
                      "no se encuentra ninguna spec activa"))

    for s in activas:
        t = trazabilidad({"spec_id": s["id"]})
        c.append(criterio("S2-02:%s" % s["id"],
                          "%s: todos los criterios tienen test que los referencia" % s["id"],
                          t["cobertura_pct"] == 100.0,
                          "sin cubrir: %s" % ", ".join(t["sin_cubrir"])))

    obligatorios = ["## Invariantes", "## Criterios de aceptación", "## Casos límite",
                    "## Fuera de alcance", "## Ambigüedades detectadas"]
    for s in activas:
        faltan = [o for o in obligatorios if not contiene(s["ruta"], o)]
        c.append(criterio("S2-03:%s" % s["id"],
                          "%s tiene los apartados obligatorios" % s["id"],
                          not faltan, "faltan: %s" % ", ".join(faltan)))

    c.append(criterio("S2-04",
                      "las ambiguedades de la spec de partida estan registradas y resueltas",
                      contiene("specs/SPEC-002-ocupacion.md", r"A-01.*banquillo")
                      and contiene("specs/SPEC-002-ocupacion.md", r"A-02.*sobreasignaci"),
                      "el apartado de ambiguedades no documenta el denominador ni el corte al 100%"))

    verde, resumen = pytest_verde()
    c.append(criterio("S2-05", "la suite completa esta en verde", verde, resumen))

    ok, detalle = mutar_y_exigir_fallo("src/abaco/reglas/ocupacion.py",
                                       "tests/test_ocupacion.py")
    c.append(criterio("S2-06",
                      "los tests fallan al mutar la implementacion (no son decorativos)",
                      ok, detalle))
    return c


if __name__ == "__main__":
    for x in verificar():
        print(("OK   " if x["ok"] else "FALLA"), x["id"], x["descripcion"], x["detalle"])
