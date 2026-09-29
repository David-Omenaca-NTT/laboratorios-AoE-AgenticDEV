"""Verificador de S1: Rebanada vertical a mano."""
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
    verde, resumen = pytest_verde()
    c.append(criterio("S1-01", "la suite esta en verde", verde, resumen))
    c.append(criterio("S1-02", "existe la maquina de estados de la demanda",
                      existe("src/abaco/dominio/estados.py")
                      and contiene("src/abaco/dominio/estados.py", r"TRANSICIONES"),
                      "falta la maquina de estados"))
    c.append(criterio("S1-03", "los ocho estados del PRD estan modelados",
                      all(contiene("src/abaco/dominio/modelos.py", e) for e in
                          ["solicitada", "aprobada", "buscando", "candidato_propuesto",
                           "aceptada", "asignada", "cerrada", "cancelada"]),
                      "faltan estados del ciclo de vida de la demanda"))
    c.append(criterio("S1-04", "los estados terminales no tienen salida",
                      contiene("src/abaco/dominio/estados.py", r"CERRADA:\s*set\(\)")
                      and contiene("src/abaco/dominio/estados.py", r"CANCELADA:\s*set\(\)"),
                      "un estado terminal con transicion de salida permite reabrir demandas"))
    c.append(criterio("S1-05", "existe Containerfile o Dockerfile multi-stage",
                      (existe("Containerfile") or existe("Dockerfile"))
                      and (contiene("Containerfile", r"(?s)FROM.*FROM")
                           or contiene("Dockerfile", r"(?s)FROM.*FROM")),
                      "no hay imagen OCI o no usa multi-stage"))
    p = ejecutar([sys.executable, "-m", "pytest", "tests/", "-q", "--no-header"])
    n = 0
    if "passed" in p.stdout:
        try:
            n = int(p.stdout.split("passed")[0].split()[-1])
        except ValueError:
            n = 0
    c.append(criterio("S1-06", "hay al menos 20 tests propios", n >= 20,
                      "tests encontrados: %d" % n))
    c.append(criterio("S1-07", "la bitacora registra el tiempo por tarea",
                      contiene("labs/S1-rebanada-vertical/bitacora.md", r"20\d\d-"),
                      "sin registro de tiempos no hay linea base para medir el salto en S2"))
    return c


if __name__ == "__main__":
    for x in verificar():
        print(("OK   " if x["ok"] else "FALLA"), x["id"], x["descripcion"], x["detalle"])
