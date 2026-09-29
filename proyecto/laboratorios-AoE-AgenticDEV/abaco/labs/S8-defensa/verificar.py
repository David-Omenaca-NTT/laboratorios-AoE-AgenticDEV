"""Verificador de S8: Defensa ante panel."""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))

from abaco_cli.verificacion import (contiene, criterio, ejecutar, existe,
                                    orden_en_historial, prueba_negativa,
                                    pytest_verde)


def verificar():
    c = []
    c.append(criterio("S8-01", "existe el guion de la defensa",
                      existe("labs/S8-defensa/defensa.md"), "falta el guion"))
    for patron, etiqueta in [("problema", "problema"), ("recorte", "recorte de alcance"),
                             ("spec", "spec"), ("arquitectura", "arquitectura"),
                             ("m[eé]tricas", "metricas"), ("gobierno", "gobierno"),
                             ("concentraci[oó]n", "concentracion")]:
        c.append(criterio("S8-02:%s" % etiqueta.replace(" ", "_"),
                          "la defensa cubre el apartado de %s" % etiqueta,
                          contiene("labs/S8-defensa/defensa.md", patron),
                          "apartado ausente en el guion"))
    c.append(criterio("S8-03",
                      "justifica el monolito modular frente a los NFR del PRD",
                      contiene("labs/S8-defensa/defensa.md", r"monolito"),
                      "el PRD pedia microservicios: hay que saber defender por que no"))
    c.append(criterio("S8-04", "incluye una decision que hoy tomarias distinta",
                      contiene("labs/S8-defensa/defensa.md", r"tomar[ií]a distinta|cambiar[ií]a"),
                      "es el mejor predictor de si aguantas una conversacion tecnica",
                      nivel="V4"))
    return c


if __name__ == "__main__":
    for x in verificar():
        print(("OK   " if x["ok"] else "FALLA"), x["id"], x["descripcion"], x["detalle"])
