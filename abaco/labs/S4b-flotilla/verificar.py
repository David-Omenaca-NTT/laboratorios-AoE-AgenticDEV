"""Verificador de S4b: Flotilla multiagente."""
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
    ruta = RAIZ / "agentes" / "flotilla" / "contrato.json"
    c.append(criterio("S4b-01", "existe el contrato de contexto de la flotilla",
                      ruta.exists(), "falta agentes/flotilla/contrato.json"))
    if not ruta.exists():
        return c
    contrato = json.loads(ruta.read_text(encoding="utf-8"))
    c.append(criterio("S4b-02", "el contrato declara resolucion de conflicto",
                      "conflicto" in contrato,
                      "no dice que pasa cuando dos agentes tocan la misma ruta"))
    nombres = [a["nombre"] for a in contrato.get("agentes", [])]
    c.append(criterio("S4b-03", "hay tres agentes declarados", len(nombres) >= 3,
                      "declarados: %s" % ", ".join(nombres)))

    staffing = [a for a in contrato.get("agentes", []) if "staffing" in a["nombre"]]
    c.append(criterio("S4b-04",
                      "el agente de staffing se declara como maximo en N2",
                      bool(staffing) and staffing[0].get("nivel_autonomia") in ("N0", "N1", "N2"),
                      "un agente que propone personas no puede pasar de N2"))
    c.append(criterio("S4b-05",
                      "los niveles difieren entre agentes y esta justificado",
                      len({a.get("nivel_autonomia") for a in contrato.get("agentes", [])}) > 1
                      and "justificacion_niveles" in contrato,
                      "si los tres tienen el mismo techo, no se ha razonado el radio de dano"))

    p = ejecutar(["git", "worktree", "list"])
    c.append(criterio("S4b-06", "se han usado worktrees aislados",
                      p.returncode == 0 and len(p.stdout.strip().splitlines()) >= 2,
                      "worktrees activos: %d" % len(p.stdout.strip().splitlines())))
    c.append(criterio("S4b-07", "existe el diagrama de flotilla",
                      existe("labs/S4b-flotilla/flotilla.md"),
                      "falta el diagrama y la descripcion del handoff"))
    return c


if __name__ == "__main__":
    for x in verificar():
        print(("OK   " if x["ok"] else "FALLA"), x["id"], x["descripcion"], x["detalle"])
