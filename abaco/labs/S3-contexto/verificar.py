"""Verificador de S3: Ingenieria de contexto y operacion de agentes."""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))

from abaco_cli.verificacion import (contiene, criterio, ejecutar, existe,
                                    orden_en_historial, prueba_negativa,
                                    pytest_verde)


SECCIONES = ["Prop[oó]sito", "Invariantes", "Verificaci[oó]n", "Convenciones",
             "L[ií]mites", "Escalado"]


def verificar():
    c = []
    faltan = [s for s in SECCIONES if not contiene("CLAUDE.md", r"#+\s*%s" % s)]
    c.append(criterio("S3-01", "CLAUDE.md tiene las seis secciones obligatorias",
                      not faltan, "faltan: %s" % ", ".join(faltan)))
    c.append(criterio("S3-02", "los invariantes son concretos y verificables",
                      contiene("CLAUDE.md", r"redondeo") and contiene("CLAUDE.md", r"auditor"),
                      "los invariantes no mencionan el redondeo unico ni la traza"))
    c.append(criterio("S3-03",
                      "el contrato declara los campos de perfil que ningun agente puede leer",
                      contiene("CLAUDE.md", r"CAMPOS_PROHIBIDOS|campos excluidos|no puede leer"),
                      "sin lista de campos excluidos el agente puede leer datos que no necesita"))
    c.append(criterio("S3-04", "hay allowlist y hooks configurados",
                      existe(".claude/settings.json"),
                      "no se encuentra configuracion de permisos"))

    def escribir_en_ruta_prohibida():
        cfg = RAIZ / ".claude" / "settings.json"
        if not cfg.exists():
            return True
        texto = cfg.read_text(encoding="utf-8")
        return not all(p in texto for p in ["manifiestos", "workflows", "legado"])

    ok, detalle = prueba_negativa(escribir_en_ruta_prohibida,
                                  "escritura en manifiestos/, workflows y legado")
    c.append(criterio("S3-05", "el control bloquea de verdad las rutas prohibidas", ok, detalle))

    c.append(criterio("S3-06", "existe la comparativa razonada entre motores",
                      existe("labs/S3-contexto/comparativa.md")
                      and contiene("labs/S3-contexto/comparativa.md", r"OpenCode"),
                      "falta la comparativa Claude Code frente a OpenCode"))
    c.append(criterio("S3-07", "hay subagentes de proposito acotado",
                      existe(".claude/agents"),
                      "no se declaran subagentes de implementacion y revision"))
    return c


if __name__ == "__main__":
    for x in verificar():
        print(("OK   " if x["ok"] else "FALLA"), x["id"], x["descripcion"], x["detalle"])
