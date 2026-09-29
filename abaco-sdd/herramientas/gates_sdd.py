"""Puertas de la modalidad SDD estricta.

Son los controles que hacen cumplir la disciplina. Sin ellos, "el codigo no se
parchea, se regenera" es una frase en un documento.

    python3 -m herramientas.gates_sdd procedencia
    python3 -m herramientas.gates_sdd deriva
    python3 -m herramientas.gates_sdd densidad
    python3 -m herramientas.gates_sdd aceptacion
    python3 -m herramientas.gates_sdd todos
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

RUTAS_GENERADAS = ("src/", "agentes/")
RUTA_ACEPTACION = "aceptacion/"
UMBRAL_DERIVA = 0.05
DENSIDAD_MIN, DENSIDAD_MAX = 1, 8

VERDE, ROJO, GRIS, RESET = "\033[32m", "\033[31m", "\033[90m", "\033[0m"


def ejecutar(comando):
    return subprocess.run(comando, cwd=RAIZ, capture_output=True, text=True)


def resultado(nombre, ok, detalle=""):
    marca = (VERDE + "OK   " + RESET) if ok else (ROJO + "FALLA" + RESET)
    print("%s %s" % (marca, nombre))
    if detalle:
        for linea in str(detalle).splitlines():
            print("      %s%s%s" % (GRIS, linea, RESET))
    return ok


# --- cambios conocidos ---------------------------------------------------------

def cambios_conocidos() -> set:
    """Identificadores de cambio validos: activos y archivados."""
    conocidos = set()
    activos = RAIZ / "openspec" / "changes"
    if activos.exists():
        for d in activos.iterdir():
            if d.is_dir() and d.name != "archive":
                conocidos.add(d.name)
    archivo = activos / "archive"
    if archivo.exists():
        for d in archivo.iterdir():
            if not d.is_dir():
                continue
            # AAAA-MM-DD-nombre
            partes = d.name.split("-", 3)
            conocidos.add(partes[3] if len(partes) == 4 else d.name)
    return conocidos


# --- gate 1: procedencia -------------------------------------------------------

def gate_procedencia() -> bool:
    """Todo commit que toca codigo generado declara el cambio que lo origina.

    Es el gate que detecta el parcheo silencioso, que es la infraccion que
    define esta modalidad.
    """
    p = ejecutar(["git", "log", "--format=%H%x1f%s%x1f%b%x1e", "--name-only"])
    if p.returncode != 0:
        return resultado("procedencia", False, "sin historial de git no se puede probar la procedencia")

    conocidos = cambios_conocidos()
    infracciones = []
    for bloque in p.stdout.split("\x1e"):
        if not bloque.strip():
            continue
        cabecera, _, ficheros = bloque.partition("\n")
        campos = cabecera.split("\x1f")
        if len(campos) < 3:
            continue
        sha, asunto, cuerpo = campos[0][-40:], campos[1], campos[2]
        tocados = [f for f in ficheros.splitlines() if f.strip()]
        rutas_generadas = [f for f in tocados if f.startswith(RUTAS_GENERADAS)]
        if not rutas_generadas:
            continue

        m = re.search(r"^Change-Id:\s*(\S+)", cuerpo, re.M)
        if not m:
            infracciones.append("%s %s: toca codigo generado sin Change-Id (%s)"
                                % (sha[:8], asunto[:45], ", ".join(rutas_generadas[:3])))
            continue
        if m.group(1) not in conocidos:
            infracciones.append("%s %s: Change-Id '%s' no existe ni activo ni archivado"
                                % (sha[:8], asunto[:35], m.group(1)))

    return resultado("procedencia: codigo generado con cambio declarado",
                     not infracciones, "\n".join(infracciones[:6]))


# --- gate 2: integridad de la bateria de aceptacion ----------------------------

def gate_aceptacion() -> bool:
    """Ningun commit marcado como generado toca la bateria de aceptacion.

    Es la puerta que sostiene toda la modalidad: si el generador puede
    modificar el examen que lo evalua, no hay evaluacion.
    """
    p = ejecutar(["git", "log", "--format=%H%x1f%b%x1e", "--name-only"])
    if p.returncode != 0:
        return resultado("aceptacion", False, "sin historial de git no se puede probar la integridad")

    infracciones = []
    for bloque in p.stdout.split("\x1e"):
        if not bloque.strip():
            continue
        cabecera, _, ficheros = bloque.partition("\n")
        campos = cabecera.split("\x1f")
        if len(campos) < 2:
            continue
        sha, cuerpo = campos[0][-40:], campos[1]
        tocados = [f for f in ficheros.splitlines()
                   if f.strip().startswith(RUTA_ACEPTACION)]
        if tocados:
            infracciones.append("%s: la bateria de aceptacion solo puede cambiarse mediante "
                                "un flujo custodiado (%s)"
                                % (sha[:8], ", ".join(tocados[:3])))

    return resultado("aceptacion: la bateria externa no la toca el generador",
                     not infracciones, "\n".join(infracciones[:6]))


# --- gate 3: deriva entre especificacion y codigo ------------------------------

def capabilities() -> dict:
    """Capability -> lista de nombres de requisito de la spec principal."""
    base = RAIZ / "openspec" / "specs"
    salida = {}
    if not base.exists():
        return salida
    for spec in base.rglob("spec.md"):
        nombre = spec.parent.relative_to(base).as_posix()
        texto = spec.read_text(encoding="utf-8")
        salida[nombre] = re.findall(r"^### Requirement:\s*(.+)$", texto, re.M)
    return salida


def modulos_generados() -> list:
    modulos = []
    for carpeta in (RAIZ / "src", RAIZ / "agentes"):
        if not carpeta.exists():
            continue
        modulos.extend(
            p.relative_to(RAIZ).as_posix() for p in carpeta.rglob("*.py")
            if p.name != "__init__.py" and "/__pycache__/" not in p.as_posix()
        )
    return modulos


def gate_deriva() -> bool:
    """Requisitos sin implementacion y modulos sin requisito que los justifique.

    La correspondencia se declara en `openspec/trazabilidad.md`, que mapea cada
    capability a sus modulos. Es un fichero humano a proposito: si lo generase
    el agente, la comprobacion no valdria nada.
    """
    mapa_ruta = RAIZ / "openspec" / "trazabilidad.md"
    if not mapa_ruta.exists():
        return resultado("deriva", False,
                         "falta openspec/trazabilidad.md, que asocia capabilities y modulos")

    texto = mapa_ruta.read_text(encoding="utf-8")
    mapa = {}
    for fila in re.findall(r"^\|\s*`([^`]+)`\s*\|\s*(.+?)\s*\|", texto, re.M):
        cap, modulos = fila
        mapa[cap] = [m.strip().strip("`") for m in modulos.split(",") if m.strip()]

    caps = capabilities()
    sin_modulo = [c for c in caps if c not in mapa or not mapa[c]]
    declarados = {m for lista in mapa.values() for m in lista}
    existentes = set(modulos_generados())
    declarados_inexistentes = sorted(m for m in declarados if not (RAIZ / m).is_file())
    huerfanos = [m for m in existentes if m not in declarados and "/legado/" not in m]

    total = len(caps) + len(existentes)
    deriva = (len(sin_modulo) + len(huerfanos) + len(declarados_inexistentes)) / total if total else 0.0

    detalle = []
    if sin_modulo:
        detalle.append("capabilities sin modulo declarado: %s" % ", ".join(sin_modulo))
    if declarados_inexistentes:
        detalle.append("modulos declarados que no existen: %s" % ", ".join(declarados_inexistentes[:5]))
    if huerfanos:
        detalle.append("modulos sin capability que los justifique: %s" % ", ".join(huerfanos[:5]))
    detalle.append("deriva %.1f%% (umbral %.0f%%)" % (deriva * 100, UMBRAL_DERIVA * 100))

    return resultado("deriva: especificacion y codigo alineados",
                     deriva <= UMBRAL_DERIVA, "\n".join(detalle))


# --- gate 4: densidad de especificacion ----------------------------------------

def gate_densidad() -> bool:
    """Escenarios por requisito dentro de un rango razonable.

    Por debajo del minimo el requisito no esta cubierto. Por encima del maximo
    nadie lo lee, y una spec que nadie lee no gobierna nada.
    """
    base = RAIZ / "openspec" / "specs"
    problemas, total_req, total_esc = [], 0, 0
    for spec in base.rglob("spec.md"):
        texto = spec.read_text(encoding="utf-8")
        bloques = re.split(r"^### Requirement:\s*", texto, flags=re.M)[1:]
        for bloque in bloques:
            nombre = bloque.splitlines()[0].strip()
            escenarios = len(re.findall(r"^#### Scenario:", bloque, re.M))
            negativos = len(re.findall(r"^#### Scenario:.*(?:no |sin |rechaz|inval|fuera|exceso|ausencia)", bloque, re.M | re.I))
            total_req += 1
            total_esc += escenarios
            if escenarios < DENSIDAD_MIN:
                problemas.append("%s / %s: %d escenarios, minimo %d"
                                 % (spec.parent.name, nombre, escenarios, DENSIDAD_MIN))
            elif escenarios > DENSIDAD_MAX:
                problemas.append("%s / %s: %d escenarios, maximo %d"
                                 % (spec.parent.name, nombre, escenarios, DENSIDAD_MAX))
            elif negativos == 0:
                problemas.append("%s / %s: falta al menos un escenario negativo"
                                 % (spec.parent.name, nombre))
    media = total_esc / total_req if total_req else 0
    detalle = problemas[:5] + ["%d requisitos, %d escenarios, media %.1f"
                               % (total_req, total_esc, media)]
    return resultado("densidad: escenarios por requisito en rango",
                     not problemas, "\n".join(detalle))


GATES = {
    "procedencia": gate_procedencia,
    "aceptacion": gate_aceptacion,
    "deriva": gate_deriva,
    "densidad": gate_densidad,
}


def main(argv=None):
    argv = argv or sys.argv[1:]
    nombre = argv[0] if argv else "todos"
    if nombre == "todos":
        print("\nPuertas de la modalidad SDD estricta\n")
        ok = all([g() for g in GATES.values()])
        print("\n%s\n" % ("todas las puertas en verde" if ok
                          else "hay puertas en rojo: el merge quedaria bloqueado"))
        return 0 if ok else 1
    if nombre not in GATES:
        print("puerta desconocida: %s. Disponibles: %s"
              % (nombre, ", ".join(GATES) + ", todos"))
        return 2
    return 0 if GATES[nombre]() else 1


if __name__ == "__main__":
    raise SystemExit(main())
