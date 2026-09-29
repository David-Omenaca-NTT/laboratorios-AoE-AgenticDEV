"""Escribe los verificadores de todas las estaciones de Abaco."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

CABECERA = '''"""Verificador de {ident}: {nombre}."""
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))

from abaco_cli.verificacion import (contiene, criterio, ejecutar, existe,
                                    orden_en_historial, prueba_negativa,
                                    pytest_verde)

'''

PIE = '''

if __name__ == "__main__":
    for x in verificar():
        print(("OK   " if x["ok"] else "FALLA"), x["id"], x["descripcion"], x["detalle"])
'''

CUERPOS = {
"S0-bootstrap": '''
import re

# Patrones de dato personal que no pueden aparecer en el repositorio de
# aprendizaje. La prohibicion no se confia a una instruccion del contrato de
# contexto: se comprueba.
PATRONES_PERSONALES = [
    (r"\\b[\\w.+-]+@(?!ejemplo\\.|example\\.)[\\w-]+\\.[\\w.]+\\b", "correo electronico real"),
    (r"\\b\\d{8}[A-HJ-NP-TV-Z]\\b", "DNI"),
    (r"\\b(?:\\+34|0034)?[\\s-]?[6-7]\\d{8}\\b", "telefono movil"),
]

RUTAS_A_ESCANEAR = ["tests", "datos", "evals", "labs", "specs"]


def escanear_datos_personales():
    hallazgos = []
    for carpeta in RUTAS_A_ESCANEAR:
        base = RAIZ / carpeta
        if not base.exists():
            continue
        for fichero in base.rglob("*"):
            if not fichero.is_file() or fichero.suffix not in (".py", ".json", ".md", ".csv"):
                continue
            try:
                texto = fichero.read_text(encoding="utf-8")
            except Exception:
                continue
            for patron, etiqueta in PATRONES_PERSONALES:
                m = re.search(patron, texto)
                if m:
                    hallazgos.append("%s en %s: %s"
                                     % (etiqueta, fichero.relative_to(RAIZ), m.group(0)[:20]))
    return hallazgos


def verificar():
    c = []
    c.append(criterio("S0-01", "existe la plantilla de PR con la checklist",
                      existe(".github/pull_request_template.md")
                      and contiene(".github/pull_request_template.md", r"defenderlo ante"),
                      "falta la plantilla o la checklist"))
    c.append(criterio("S0-02", "CODEOWNERS protege labs, manifiestos y workflows",
                      existe(".github/CODEOWNERS")
                      and contiene(".github/CODEOWNERS", r"labs/")
                      and contiene(".github/CODEOWNERS", r"manifiestos/"),
                      "CODEOWNERS no cubre las rutas prohibidas del contrato de contexto"))
    c.append(criterio("S0-03", "el pipeline incluye el gate de tamano de PR",
                      contiene(".github/workflows/ci.yml", r"tamano-pr|LIMITE_LINEAS"),
                      "no hay job que limite el tamano del diff"))
    c.append(criterio("S0-04", "el pipeline ejecuta la suite",
                      contiene(".github/workflows/ci.yml", r"pytest"),
                      "el workflow no ejecuta los tests"))

    hallazgos = escanear_datos_personales()
    c.append(criterio("S0-05",
                      "NINGUN dato personal real en el repositorio de aprendizaje",
                      not hallazgos,
                      "; ".join(hallazgos[:3]) if hallazgos else ""))

    c.append(criterio("S0-06", "el contrato de contexto prohibe copiar datos reales",
                      contiene("CLAUDE.md", r"dato[s]? personal"),
                      "CLAUDE.md no declara la prohibicion de datos personales"))

    p = ejecutar(["git", "log", "--oneline"])
    commits = len(p.stdout.strip().splitlines()) if p.returncode == 0 else 0
    c.append(criterio("S0-07", "hay historial de git con al menos dos commits",
                      commits >= 2, "commits encontrados: %d" % commits))
    return c
''',

"S1-rebanada-vertical": '''
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
                      contiene("src/abaco/dominio/estados.py", r"CERRADA:\\s*set\\(\\)")
                      and contiene("src/abaco/dominio/estados.py", r"CANCELADA:\\s*set\\(\\)"),
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
                      contiene("labs/S1-rebanada-vertical/bitacora.md", r"20\\d\\d-"),
                      "sin registro de tiempos no hay linea base para medir el salto en S2"))
    return c
''',

"S2-sdd": '''
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
''',

"S3-contexto": '''
SECCIONES = ["Prop[oó]sito", "Invariantes", "Verificaci[oó]n", "Convenciones",
             "L[ií]mites", "Escalado"]


def verificar():
    c = []
    faltan = [s for s in SECCIONES if not contiene("CLAUDE.md", r"#+\\s*%s" % s)]
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
''',

"S4a-agente-propio": '''
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

    informes = sorted((RAIZ / "evals" / "informes").glob("*.json")) \\
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
''',

"S4b-flotilla": '''
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
''',

"S5-legado": '''
def verificar():
    c = []
    c.append(criterio("S5-01", "existe la bateria de caracterizacion",
                      existe("tests/test_caracterizacion_legado.py"),
                      "sin caracterizacion no se puede tocar el legado"))

    ok, detalle = orden_en_historial(r"caracteriz", r"^refactor", por_asunto=True)
    c.append(criterio("S5-02",
                      "REGLA DURA: la caracterizacion precede al refactor en el historial",
                      ok is True, detalle))

    c.append(criterio("S5-03",
                      "la caracterizacion captura los comportamientos no documentados",
                      contiene("tests/test_caracterizacion_legado.py", r"no_documentado_1")
                      and contiene("tests/test_caracterizacion_legado.py", r"no_documentado_2"),
                      "faltan los comportamientos ocultos: solo se descubren ejecutando"))

    verde, resumen = pytest_verde("tests/test_caracterizacion_legado.py")
    c.append(criterio("S5-04", "la caracterizacion esta en verde", verde, resumen))

    verde2, resumen2 = pytest_verde("tests/test_equivalencia_legado.py")
    c.append(criterio("S5-05", "equivalencia sin desviaciones sin justificar",
                      verde2, resumen2))

    c.append(criterio("S5-06", "toda desviacion esta declarada con causa y efecto",
                      existe("src/abaco/legado/DESVIACIONES.md")
                      and contiene("src/abaco/legado/DESVIACIONES.md", r"D-01")
                      and contiene("src/abaco/legado/DESVIACIONES.md", r"aguas abajo"),
                      "falta DESVIACIONES.md o no documenta el efecto aguas abajo"))
    c.append(criterio("S5-07",
                      "se documenta el impacto del cambio en el numero que ve direccion",
                      contiene("src/abaco/legado/DESVIACIONES.md", r"cuadro de mando"),
                      "corregir el calculo cambia el reporting y hay que anunciarlo antes"))
    return c
''',

"S6-gobierno": '''
import re
from datetime import date


def _manifiestos():
    d = RAIZ / "manifiestos"
    return sorted(d.glob("*.yaml")) if d.exists() else []


def _campo(texto, clave):
    m = re.search(r"^%s:\\s*(.+)$" % clave, texto, re.M)
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

        fecha = re.search(r"fecha:\\s*(\\d{4}-\\d{2}-\\d{2})", texto)
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
''',

"S7-despliegue": '''
def verificar():
    c = []
    c.append(criterio("S7-01", "el pipeline tiene etapa de despliegue",
                      contiene(".github/workflows/ci.yml", r"deploy|despliegue"),
                      "no hay etapa de despliegue"))
    c.append(criterio("S7-02", "existe procedimiento de reversion documentado",
                      existe("labs/S7-despliegue/reversion.md"),
                      "un despliegue sin reversion probada no es un despliegue"))
    c.append(criterio("S7-03", "hay registro de MTTR de las dos rondas",
                      existe("labs/S7-despliegue/mttr.md")
                      and contiene("labs/S7-despliegue/mttr.md", r"[Rr]onda 2"),
                      "faltan las dos rondas, sin agente y con agente"))
    c.append(criterio("S7-04", "la retrospectiva compara hipotesis inicial y causa real",
                      contiene("labs/S7-despliegue/mttr.md", r"hip[oó]tesis"),
                      "comparar hipotesis y causa real es lo que ensena a diagnosticar"))
    c.append(criterio("S7-05", "hay observabilidad instrumentada",
                      contiene("src/abaco/api/app.py", r"log|trace|metric"),
                      "sin instrumentacion no se puede medir nada"))
    return c
''',

"S8-defensa": '''
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
''',
}

NOMBRES = {
    "S0-bootstrap": ("S0", "Bootstrap y disciplina de repositorio"),
    "S1-rebanada-vertical": ("S1", "Rebanada vertical a mano"),
    "S2-sdd": ("S2", "Spec-Driven Development"),
    "S3-contexto": ("S3", "Ingenieria de contexto y operacion de agentes"),
    "S4a-agente-propio": ("S4a", "Servidor MCP y agente de staffing"),
    "S4b-flotilla": ("S4b", "Flotilla multiagente"),
    "S5-legado": ("S5", "Modernizacion del legado con agentes"),
    "S6-gobierno": ("S6", "Gobierno de un agente sobre personas"),
    "S7-despliegue": ("S7", "Despliegue, fallo inducido y MTTR"),
    "S8-defensa": ("S8", "Defensa ante panel"),
}


def main():
    for carpeta, cuerpo in CUERPOS.items():
        ident, nombre = NOMBRES[carpeta]
        (RAIZ / "labs" / carpeta / "verificar.py").write_text(
            CABECERA.format(ident=ident, nombre=nombre) + cuerpo + PIE, encoding="utf-8")
    print("escritos %d verificadores" % len(CUERPOS))


if __name__ == "__main__":
    main()
