"""Equivalencia entre la calculadora heredada y el motor nuevo.

Regla de la estacion S5: cero desviaciones NO justificadas sobre el corpus. Una
desviacion solo es aceptable si esta declarada en `legado/DESVIACIONES.md` con
su categoria, su causa y su efecto aguas abajo.

Este test produce el informe que se entrega en S5.

cubre: LEG-EQU (equivalencia del legado, no es una spec)
"""
import json
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from abaco.legado import calculadora_utilizacion_v1 as legado
from abaco.reglas.ocupacion import utilizacion, utilizacion_agregada
from agentes.staffing.agente import cargar_contexto

RAIZ = Path(__file__).resolve().parents[1]
DESDE, HASTA = date(2026, 7, 1), date(2026, 7, 31)
TOLERANCIA = Decimal("0.01")

CATEGORIAS = {
    "D-01": "banquillo excluido entero del calculo global",
    "D-02": "promedio de porcentajes ya redondeados en lugar de agregar",
    "D-03": "la asignacion computa durante ausencia no trabajable",
    "D-04": "la sobreasignacion no se corta en el 100%",
}


@pytest.fixture(scope="module")
def contexto():
    return cargar_contexto()


@pytest.fixture(scope="module")
def bruto():
    return json.loads((RAIZ / "datos" / "corpus_sintetico.json").read_text(encoding="utf-8"))


def clasificar(persona, contexto, viejo, nuevo):
    """Atribuye cada desviacion individual a una categoria declarada."""
    ausencias = [a for a in contexto["ausencias"] if a.persona_id == persona.persona_id]
    asignaciones = [a for a in contexto["asignaciones"] if a.persona_id == persona.persona_id]
    no_trabajable = any(a.tipo.value in ("vacaciones", "festivo", "baja")
                        and a.solapa(DESDE, HASTA) and a.aprobada for a in ausencias)
    solapadas = sum(a.dedicacion_pct for a in asignaciones if a.solapa(DESDE, HASTA))
    if no_trabajable and viejo > nuevo:
        return "D-03"
    if solapadas > 100:
        return "D-04"
    return None


def test_equivalencia_individual_solo_con_desviaciones_declaradas(contexto, bruto):
    legado._CACHE.clear()
    r = legado.calcular(bruto, DESDE.isoformat(), HASTA.isoformat())
    desviaciones = {c: 0 for c in CATEGORIAS}
    sin_clasificar, iguales = [], 0

    for persona in contexto["personas"]:
        viejo = Decimal(str(r["detalle"][persona.persona_id]))
        nuevo = utilizacion(persona, contexto["asignaciones"], contexto["ausencias"],
                            DESDE, HASTA)
        if abs(viejo - nuevo) <= TOLERANCIA:
            iguales += 1
            continue
        categoria = clasificar(persona, contexto, viejo, nuevo)
        if categoria:
            desviaciones[categoria] += 1
        else:
            sin_clasificar.append(persona.persona_id)

    informe = {"personas": len(contexto["personas"]), "coincidentes": iguales,
               "desviaciones_justificadas": desviaciones,
               "desviaciones_sin_justificar": sin_clasificar}
    destino = RAIZ / ".abaco" / "informe_equivalencia.json"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(informe, ensure_ascii=False, indent=2), encoding="utf-8")

    assert not sin_clasificar, ("desviaciones sin categoria declarada: %d, %s"
                                % (len(sin_clasificar), sin_clasificar[:5]))
    assert desviaciones["D-03"] > 0, "el defecto de vacaciones debe aflorar en el corpus"


def test_el_global_del_legado_es_optimista_por_excluir_el_banquillo(contexto, bruto):
    """D-01 y D-02 juntas. Es la desviacion que mas importa porque el numero
    global es el que ve direccion."""
    legado._CACHE.clear()
    viejo = Decimal(str(legado.calcular(bruto, DESDE.isoformat(),
                                        HASTA.isoformat())["utilizacion_global"]))
    nuevo = utilizacion_agregada(contexto["personas"], contexto["asignaciones"],
                                 contexto["ausencias"], DESDE, HASTA)
    assert viejo > nuevo, "el legado infla el numero global"
    informe = RAIZ / ".abaco" / "informe_equivalencia.json"
    if informe.exists():
        datos = json.loads(informe.read_text(encoding="utf-8"))
        datos["global_legado"] = str(viejo)
        datos["global_nuevo"] = str(nuevo)
        datos["diferencia_puntos"] = str(viejo - nuevo)
        informe.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")


def test_sin_ausencias_ni_sobreasignacion_ambos_motores_coinciden(contexto, bruto):
    """El nucleo del calculo es el mismo. Si esto falla, el refactor rompio algo
    que no tenia que ver con las desviaciones declaradas."""
    legado._CACHE.clear()
    r = legado.calcular(bruto, DESDE.isoformat(), HASTA.isoformat())
    comprobados = 0
    for persona in contexto["personas"]:
        ausencias = [a for a in contexto["ausencias"]
                     if a.persona_id == persona.persona_id and a.solapa(DESDE, HASTA)]
        asignaciones = [a for a in contexto["asignaciones"]
                        if a.persona_id == persona.persona_id and a.solapa(DESDE, HASTA)]
        if ausencias or sum(a.dedicacion_pct for a in asignaciones) > 100:
            continue
        if not asignaciones:
            continue
        viejo = Decimal(str(r["detalle"][persona.persona_id]))
        nuevo = utilizacion(persona, contexto["asignaciones"], contexto["ausencias"],
                            DESDE, HASTA)
        assert abs(viejo - nuevo) <= TOLERANCIA, persona.persona_id
        comprobados += 1
    assert comprobados > 20
