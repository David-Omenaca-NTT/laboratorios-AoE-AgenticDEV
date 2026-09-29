"""Verificador de S6: Gobierno de un agente sobre personas."""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))

from abaco_cli.verificacion import (contiene, criterio, ejecutar, existe,
                                    orden_en_historial, prueba_negativa,
                                    pytest_verde)


import re
from datetime import date


def _manifiestos():
    d = RAIZ / "manifiestos"
    return sorted(d.glob("*.yaml")) if d.exists() else []


def _campo(texto, clave):
    m = re.search(r"^%s:\s*(.+)$" % clave, texto, re.M)
    return m.group(1).strip() if m else None


OBLIGATORIOS = ["agente", "version", "propietario_humano", "nivel_autonomia",
                "herramientas", "evaluacion", "coste", "reversion",
                "personas_afectadas", "explicabilidad", "via_de_contestacion",
                "veto_humano", "vigilancia_concentracion", "datos_prohibidos"]


def verificar():
    c = []
    manifiestos = _manifiestos()
    c.append(criterio("S6-01", "existe un Agent Release Manifest por agente",
                      len(manifiestos) >= 1,
                      "manifiestos encontrados: %d" % len(manifiestos)))

    for m in manifiestos:
        texto = m.read_text(encoding="utf-8")
        faltan = [o for o in OBLIGATORIOS if o + ":" not in texto]
        c.append(criterio("S6-02:%s" % m.stem,
                          "%s tiene los catorce apartados obligatorios" % m.name,
                          not faltan, "faltan: %s" % ", ".join(faltan)))

        nivel = _campo(texto, "nivel_autonomia")
        propone_personas = "staffing" in m.stem or "personas_afectadas" in texto
        techo = ("N0", "N1", "N2") if propone_personas else ("N0", "N1", "N2", "N3")
        c.append(criterio("S6-03:%s" % m.stem,
                          "%s declara un nivel dentro de su techo" % m.name,
                          nivel in techo,
                          "nivel %s. Un agente que propone personas no pasa de N2: el "
                          "techo lo fija la reversibilidad del dano, no la precision" % nivel))

        fecha = re.search(r"fecha:\s*(\d{4}-\d{2}-\d{2})", texto)
        vigente = False
        if fecha:
            vigente = (date.today() - date.fromisoformat(fecha.group(1))).days <= 30
        c.append(criterio("S6-04:%s" % m.stem,
                          "%s referencia una evaluacion de menos de 30 dias" % m.name,
                          vigente, "fecha declarada: %s" % (fecha.group(1) if fecha else "ninguna")))

    c.append(criterio("S6-05", "el pipeline tiene el gate de manifiesto",
                      existe(".github/workflows/gate-manifiesto.yml"),
                      "sin gate, el manifiesto es documentacion y no gobierno"))

    def gate_permite_n4():
        gate = RAIZ / ".github" / "workflows" / "gate-manifiesto.yml"
        if not gate.exists():
            return True
        texto = gate.read_text(encoding="utf-8")
        return not ("N4" in texto and ("sys.exit(1" in texto or "exit 1" in texto))

    ok, detalle = prueba_negativa(gate_permite_n4, "manifiesto que declara N4")
    c.append(criterio("S6-06", "el gate rechaza un manifiesto que declare N4", ok, detalle))

    def agente_lee_campo_prohibido():
        agente = RAIZ / "agentes" / "staffing" / "agente.py"
        if not agente.exists():
            return True
        texto = agente.read_text(encoding="utf-8")
        return "CAMPOS_PROHIBIDOS" not in texto

    ok2, detalle2 = prueba_negativa(agente_lee_campo_prohibido,
                                    "lectura de campos de perfil excluidos")
    c.append(criterio("S6-07", "el agente declara y respeta los campos excluidos",
                      ok2, detalle2))

    c.append(criterio("S6-08", "existe el informe de concentracion comentado",
                      existe("labs/S6-gobierno/concentracion.md"),
                      "medir el sesgo del propio agente es entregable de la estacion"))
    c.append(criterio("S6-09", "existe el informe de coste por propuesta verificada",
                      existe("labs/S6-gobierno/coste.md"),
                      "falta la traduccion de tokens a unidad de negocio"))
    c.append(criterio("S6-10",
                      "existe la argumentacion escrita sobre por que NO se llega a N4",
                      existe("labs/S6-gobierno/n4.md"), "falta el analisis", nivel="V3"))
    return c


if __name__ == "__main__":
    for x in verificar():
        print(("OK   " if x["ok"] else "FALLA"), x["id"], x["descripcion"], x["detalle"])
