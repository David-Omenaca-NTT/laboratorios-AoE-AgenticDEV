# GENERADO DESDE ESPECIFICACION. NO EDITAR A MANO.
# Capability: agente-staffing
# Cambio de origen: e6-agente-propuesta-staffing
# Si algo esta mal aqui, esta mal en la spec. Corrige la spec y regenera.
"""Agente de propuesta de staffing.

Recibe una demanda y propone candidatos ordenados para cada posicion, con la
evidencia de por que cada uno entra y por que cada descartado no entra.

Decision de arquitectura, y aqui deja de ser una preferencia de ingenieria para
ser un requisito de gobierno:

  El nucleo es DETERMINISTA. El filtrado por restricciones duras, la
  comprobacion de disponibilidad, el encaje de categoria y toda la aritmetica de
  ocupacion se calculan sin modelo. El modelo interviene solo para redactar la
  explicacion, y solo sobre candidatos que ya han pasado todos los filtros.

  Motivo: la parte que puede hacer dano tiene que ser auditable linea a linea.
  Una recomendacion que no se puede reproducir no se puede defender ante la
  persona que no fue propuesta.

Techo de autonomia: N2. Este agente PROPONE; la decision corresponde a una
persona. Nunca crea asignaciones. El techo no lo fija la precision del modelo,
lo fija que aqui hay carreras de por medio.

Uso:
    python3 -m agentes.staffing.agente --demanda evals/dorado_ejemplo/oro-001.json
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from datetime import date
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))

from abaco.dominio.modelos import (Asignacion, Ausencia, CategoriaVigencia,  # noqa: E402
                                   Modalidad, Persona, Posicion, Skill,
                                   TipoDisponibilidad)
from abaco.reglas.motor import evaluar_candidato  # noqa: E402
from abaco.reglas.ocupacion import (capacidad_disponible, desviacion_sobre_objetivo,  # noqa: E402
                                    utilizacion)
from abaco.reglas.politicas import cargar_politica, catalogo_vigente_en  # noqa: E402

# Campos del perfil que el agente NO puede leer. Declarado en el manifiesto y
# comprobado por prueba negativa en el verificador de S6.
CAMPOS_PROHIBIDOS = ("nombre", "pais", "oficina", "fecha_nacimiento", "genero",
                     "foto", "email", "telefono")


@dataclass
class Candidato:
    persona_id: str
    categoria_registrada: str
    distancia_seniority: int
    skill: str
    nivel: int
    nivel_pedido: int
    capacidad_libre_pct: int
    utilizacion_actual: str
    utilizacion_resultante: str
    desviacion_sobre_objetivo: str
    en_banquillo: bool
    puntuacion: str


@dataclass
class Descartado:
    persona_id: str
    motivos: list


@dataclass
class PropuestaPosicion:
    rol: str
    categoria_pedida: str
    skill_pedido: str
    nivel_minimo: int
    dedicacion_pct: int = 100
    candidatos: list = field(default_factory=list)
    descartados: list = field(default_factory=list)


@dataclass
class Propuesta:
    demanda_id: str
    proyecto: str
    desde: str
    hasta: str
    version_catalogo: str
    version_politica: str
    posiciones: list = field(default_factory=list)
    explicacion: str = ""
    nivel_autonomia: str = "N2"
    decide: str = "resource manager. El agente no crea asignaciones."

    def a_dict(self):
        return asdict(self)


# --- carga del contexto --------------------------------------------------------

def _persona(bruto: dict) -> Persona:
    return Persona(
        persona_id=bruto["persona_id"], nombre="", pais="", oficina="",
        fecha_alta=date.fromisoformat(bruto["fecha_alta"]),
        fecha_baja=date.fromisoformat(bruto["fecha_baja"]) if bruto.get("fecha_baja") else None,
        historico_categoria=[
            CategoriaVigencia(h["codigo_categoria"], date.fromisoformat(h["desde"]),
                              date.fromisoformat(h["hasta"]) if h.get("hasta") else None)
            for h in bruto["historico_categoria"]],
        skills=[Skill(s["codigo"], s["nivel"],
                      date.fromisoformat(s["ultimo_uso"]) if s.get("ultimo_uso") else None)
                for s in bruto.get("skills", [])])


def _asignacion(b: dict) -> Asignacion:
    return Asignacion(
        asignacion_id=b["asignacion_id"], persona_id=b["persona_id"],
        proyecto=b["proyecto"], rol=b.get("rol", ""),
        desde=date.fromisoformat(b["desde"]), hasta=date.fromisoformat(b["hasta"]),
        dedicacion_pct=b["dedicacion_pct"], modalidad=Modalidad(b.get("modalidad", "porcentual")),
        categoria_registrada=b.get("categoria_registrada", ""),
        version_catalogo=b.get("version_catalogo", ""),
        version_politica=b.get("version_politica", ""),
        confirmada=b.get("confirmada", True))


def _ausencia(b: dict) -> Ausencia:
    return Ausencia(persona_id=b["persona_id"], tipo=TipoDisponibilidad(b["tipo"]),
                    desde=date.fromisoformat(b["desde"]),
                    hasta=date.fromisoformat(b["hasta"]),
                    aprobada=b.get("aprobada", True))


def cargar_contexto(ruta: Path = None) -> dict:
    ruta = ruta or (RAIZ / "datos" / "corpus_sintetico.json")
    bruto = json.loads(ruta.read_text(encoding="utf-8"))
    return {
        "personas": [_persona(p) for p in bruto["personas"]],
        "asignaciones": [_asignacion(a) for a in bruto["asignaciones"]],
        "ausencias": [_ausencia(a) for a in bruto["ausencias"]],
    }


# --- nucleo determinista -------------------------------------------------------

def puntuar(persona: Persona, posicion: Posicion, contexto: dict, catalogo,
            desde: date, hasta: date) -> Decimal:
    """Puntuacion de encaje, determinista y explicable.

    Deliberadamente simple y sin coste: encaje de skill, ajuste de categoria y
    hueco de ocupacion respecto del objetivo de su categoria. Cada sumando se
    puede enseniar a la persona que pregunte por que no fue propuesta.
    """
    skill = persona.skill(posicion.skill)
    nivel = Decimal(skill.nivel if skill else 0)
    exceso_nivel = max(Decimal(0), nivel - Decimal(posicion.nivel_minimo))

    codigo = persona.categoria_en(desde)
    suya = catalogo.categoria(codigo)
    pedida = catalogo.categoria(posicion.codigo_categoria)
    # Penaliza el sobredimensionado: un Director en una posicion de Consultor
    # encaja, pero es un mal uso del pool.
    exceso_categoria = Decimal(suya.orden_seniority - pedida.orden_seniority)

    desviacion = desviacion_sobre_objetivo(persona, catalogo,
                                           contexto["asignaciones"],
                                           contexto["ausencias"], desde, hasta)
    # Por debajo de su objetivo suma: el agente reparte hacia quien tiene hueco.
    hueco = max(Decimal(0), -desviacion) / Decimal(10)

    return (nivel * Decimal(2) + exceso_nivel + hueco
            - exceso_categoria * Decimal("1.5"))


def proponer(demanda: dict, contexto: dict, maximo: int = 3) -> Propuesta:
    desde = date.fromisoformat(demanda["desde"])
    hasta = date.fromisoformat(demanda["hasta"])
    catalogo = catalogo_vigente_en(desde, RAIZ / "politicas" / "categorias")
    politica = cargar_politica("POL-2026", RAIZ / "politicas" / "capacidad")

    propuesta = Propuesta(
        demanda_id=demanda["demanda_id"], proyecto=demanda["proyecto"],
        desde=demanda["desde"], hasta=demanda["hasta"],
        version_catalogo=catalogo.version, version_politica=politica.version)

    for pos in demanda["posiciones"]:
        posicion = Posicion(rol=pos["rol"], codigo_categoria=pos["codigo_categoria"],
                            skill=pos["skill"], nivel_minimo=pos["nivel_minimo"],
                            dedicacion_pct=pos["dedicacion_pct"])
        bloque = PropuestaPosicion(rol=posicion.rol,
                                   categoria_pedida=posicion.codigo_categoria,
                                   skill_pedido=posicion.skill,
                                   nivel_minimo=posicion.nivel_minimo,
                                   dedicacion_pct=posicion.dedicacion_pct)
        aptos = []
        for persona in contexto["personas"]:
            veredicto = evaluar_candidato(persona, posicion, desde, hasta, catalogo,
                                          politica, contexto["asignaciones"],
                                          contexto["ausencias"])
            if not veredicto.apta:
                bloque.descartados.append(Descartado(persona.persona_id,
                                                     list(veredicto.motivos)))
                continue
            aptos.append((puntuar(persona, posicion, contexto, catalogo, desde, hasta),
                          persona))

        aptos.sort(key=lambda x: (-x[0], x[1].persona_id))
        for puntos, persona in aptos[:maximo]:
            skill = persona.skill(posicion.skill)
            codigo = persona.categoria_en(desde)
            suya = catalogo.categoria(codigo)
            pedida = catalogo.categoria(posicion.codigo_categoria)
            ocupada = sum(a.dedicacion_pct for a in contexto["asignaciones"]
                          if a.persona_id == persona.persona_id and a.solapa(desde, hasta))
            actual = utilizacion(persona, contexto["asignaciones"],
                                 contexto["ausencias"], desde, hasta)
            resultante = min(Decimal(100), actual + Decimal(posicion.dedicacion_pct))
            bloque.candidatos.append(Candidato(
                persona_id=persona.persona_id,
                categoria_registrada=codigo,
                distancia_seniority=suya.orden_seniority - pedida.orden_seniority,
                skill=posicion.skill, nivel=skill.nivel, nivel_pedido=posicion.nivel_minimo,
                capacidad_libre_pct=max(0, 100 - ocupada),
                utilizacion_actual=str(actual),
                utilizacion_resultante=str(resultante),
                desviacion_sobre_objetivo=str(desviacion_sobre_objetivo(
                    persona, catalogo, contexto["asignaciones"],
                    contexto["ausencias"], desde, hasta)),
                en_banquillo=ocupada == 0,
                puntuacion=str(puntos.quantize(Decimal("0.01")))))
        propuesta.posiciones.append(bloque)

    propuesta.explicacion = JuezOffline().explicar(propuesta)
    return propuesta


class JuezOffline:
    """Redacta la explicacion sin modelo. Modo por defecto y sin coste."""

    def explicar(self, p: Propuesta) -> str:
        partes = []
        for bloque in p.posiciones:
            if not bloque.candidatos:
                partes.append(
                    "Para %s no hay ningun candidato que cumpla las restricciones "
                    "duras: %d personas descartadas." % (bloque.rol, len(bloque.descartados)))
                continue
            primero = bloque.candidatos[0]
            partes.append(
                "Para %s se propone %s en primer lugar: categoria %s frente a %s "
                "pedida, %s nivel %d sobre %d exigido, %d%% de capacidad libre y "
                "utilizacion %s frente al objetivo de su categoria. Se descartaron "
                "%d personas."
                % (bloque.rol, primero.persona_id, primero.categoria_registrada,
                   bloque.categoria_pedida, bloque.skill_pedido, primero.nivel,
                   bloque.nivel_minimo, primero.capacidad_libre_pct,
                   primero.desviacion_sobre_objetivo, len(bloque.descartados)))
        partes.append("El agente propone. La decision es del resource manager.")
        return " ".join(partes)


class JuezClaude:
    """Explicacion redactada por modelo. El orden y los filtros llegan ya
    calculados: el modelo no decide a quien se propone."""

    def __init__(self, modelo="claude-sonnet-4-6", cliente=None):
        self.modelo, self.cliente = modelo, cliente

    def explicar(self, p: Propuesta) -> str:
        if self.cliente is None:
            try:
                import anthropic
                self.cliente = anthropic.Anthropic()
            except Exception:
                return JuezOffline().explicar(p) + " [juez offline: sin cliente]"
        prompt = (
            "Redacta en tres o cuatro frases, en espanol y sin adornos, por que se "
            "propone a estos candidatos. No cambies el orden, no anadas ni quites "
            "candidatos y no inventes motivos que no esten en los datos.\n\n"
            + json.dumps(p.a_dict(), ensure_ascii=False, indent=2))
        r = self.cliente.messages.create(model=self.modelo, max_tokens=500,
                                         messages=[{"role": "user", "content": prompt}])
        return "".join(b.text for b in r.content if getattr(b, "type", "") == "text")


def formatear_markdown(p: Propuesta) -> str:
    lineas = ["## Propuesta de staffing para %s" % p.demanda_id, "",
              "Proyecto `%s`, del %s al %s" % (p.proyecto, p.desde, p.hasta),
              "Catalogo `%s`, politica `%s`" % (p.version_catalogo, p.version_politica),
              "", "> Nivel de autonomia N2: %s" % p.decide, ""]
    for bloque in p.posiciones:
        lineas += ["### %s (%s, %s nivel %d o superior)"
                   % (bloque.rol, bloque.categoria_pedida, bloque.skill_pedido,
                      bloque.nivel_minimo), ""]
        if not bloque.candidatos:
            lineas += ["Ningun candidato cumple las restricciones duras.", ""]
        else:
            lineas += ["| # | Persona | Categoria | Nivel | Libre | Utilizacion | Desv. objetivo | Banquillo |",
                       "|---|---------|-----------|-------|-------|-------------|----------------|-----------|"]
            for i, c in enumerate(bloque.candidatos, 1):
                lineas.append("| %d | %s | %s | %d | %d%% | %s%% | %s | %s |"
                              % (i, c.persona_id, c.categoria_registrada, c.nivel,
                                 c.capacidad_libre_pct, c.utilizacion_actual,
                                 c.desviacion_sobre_objetivo,
                                 "si" if c.en_banquillo else "no"))
            lineas.append("")
        motivos = {}
        for d in bloque.descartados:
            for m in d.motivos:
                motivos[m] = motivos.get(m, 0) + 1
        if motivos:
            lineas += ["Descartados por motivo: "
                       + ", ".join("%s (%d)" % (m, n) for m, n in sorted(motivos.items())), ""]
    lineas += ["### Explicacion", "", p.explicacion]
    return "\n".join(lineas)


def principal(argv=None):
    ap = argparse.ArgumentParser(description="Agente de propuesta de staffing")
    ap.add_argument("--demanda", required=True)
    ap.add_argument("--contexto", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    demanda = json.loads(Path(args.demanda).read_text(encoding="utf-8"))
    contexto = cargar_contexto(Path(args.contexto) if args.contexto else None)
    propuesta = proponer(demanda, contexto)
    print(json.dumps(propuesta.a_dict(), ensure_ascii=False, indent=2)
          if args.json else formatear_markdown(propuesta))
    return 0


if __name__ == "__main__":
    raise SystemExit(principal())
