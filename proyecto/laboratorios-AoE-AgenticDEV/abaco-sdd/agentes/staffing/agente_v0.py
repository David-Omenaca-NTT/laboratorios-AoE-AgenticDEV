"""Iteracion 0 del agente de staffing. ES LA QUE LLEVA EL REPO DE APRENDIZAJE.

Enfoque ingenuo y muy comun: buscar a quien tenga el skill y ordenar por
disponibilidad. No comprueba categoria, no comprueba ausencias aprobadas y no
comprueba solape real de asignaciones, solo mira si tiene alguna asignacion que
empiece dentro del periodo.

No es un error de diseno: es el punto de partida del student en S4a. La estacion
consiste en medirlo contra el conjunto dorado, ver cuantas restricciones duras
viola y llegar a la version final con la mejora documentada.
"""
from __future__ import annotations

import sys
from datetime import date
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "src"))

from agentes.staffing.agente import (Candidato, Descartado, Propuesta,  # noqa: E402
                                     PropuestaPosicion)
from abaco.reglas.politicas import cargar_politica, catalogo_vigente_en  # noqa: E402


def proponer_v0(demanda: dict, contexto: dict, maximo: int = 3) -> Propuesta:
    desde = date.fromisoformat(demanda["desde"])
    hasta = date.fromisoformat(demanda["hasta"])
    catalogo = catalogo_vigente_en(desde, RAIZ / "politicas" / "categorias")
    politica = cargar_politica("POL-2026", RAIZ / "politicas" / "capacidad")

    propuesta = Propuesta(
        demanda_id=demanda["demanda_id"], proyecto=demanda["proyecto"],
        desde=demanda["desde"], hasta=demanda["hasta"],
        version_catalogo=catalogo.version, version_politica=politica.version)

    for pos in demanda["posiciones"]:
        bloque = PropuestaPosicion(rol=pos["rol"], categoria_pedida=pos["codigo_categoria"],
                                   skill_pedido=pos["skill"], nivel_minimo=pos["nivel_minimo"],
                                   dedicacion_pct=pos["dedicacion_pct"])
        candidatos = []
        for persona in contexto["personas"]:
            skill = persona.skill(pos["skill"])
            if skill is None:
                bloque.descartados.append(Descartado(persona.persona_id, ["no tiene el skill"]))
                continue
            # v0: mira si "parece" libre, comprobando solo la fecha de inicio
            ocupada = sum(a.dedicacion_pct for a in contexto["asignaciones"]
                          if a.persona_id == persona.persona_id and desde <= a.desde <= hasta)
            candidatos.append((ocupada, -skill.nivel, persona))
        candidatos.sort(key=lambda x: (x[0], x[1], x[2].persona_id))
        for ocupada, _, persona in candidatos[:maximo]:
            skill = persona.skill(pos["skill"])
            bloque.candidatos.append(Candidato(
                persona_id=persona.persona_id,
                categoria_registrada=persona.categoria_en(desde) or "?",
                distancia_seniority=0, skill=pos["skill"], nivel=skill.nivel,
                nivel_pedido=pos["nivel_minimo"],
                capacidad_libre_pct=max(0, 100 - ocupada),
                utilizacion_actual="0.00", utilizacion_resultante="0.00",
                desviacion_sobre_objetivo="0.00", en_banquillo=ocupada == 0,
                puntuacion=str(Decimal(skill.nivel))))
        propuesta.posiciones.append(bloque)
    propuesta.explicacion = "Candidatos con el skill pedido, ordenados por disponibilidad aparente."
    return propuesta
