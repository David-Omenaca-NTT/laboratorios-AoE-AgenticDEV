"""Caracterizacion del modulo heredado.

Estos tests NO afirman que el comportamiento sea correcto. Afirman cual es.
Es la red de seguridad que permite refactorizar sin romper nada por accidente,
y es la que deja al descubierto los dos comportamientos no documentados.

Regla dura de S5: estos tests se escriben y se commitean ANTES de tocar una
sola linea de `legado/`. El verificador comprueba el orden en el historial.

cubre: LEG-CAR (caracterizacion del legado, no es una spec)
"""
import json
from pathlib import Path

import pytest

from abaco.legado import calculadora_utilizacion_v1 as legado

RAIZ = Path(__file__).resolve().parents[1]
JUL_D, JUL_H = "2026-07-01", "2026-07-31"


@pytest.fixture(autouse=True)
def limpiar_cache():
    """El modulo heredado cachea por periodo, no por conjunto de datos. Sin
    limpiar, dos escenarios distintos del mismo mes devuelven el primero.
    Descubrirlo es parte del ejercicio."""
    legado._CACHE.clear()
    yield
    legado._CACHE.clear()


def persona(pid, pais="ES"):
    return {"persona_id": pid, "pais": pais}


def asg(pid, desde=JUL_D, hasta=JUL_H, ded=100):
    return {"persona_id": pid, "desde": desde, "hasta": hasta, "dedicacion_pct": ded}


def aus(pid, tipo, desde, hasta, aprobada=True):
    return {"persona_id": pid, "tipo": tipo, "desde": desde, "hasta": hasta,
            "aprobada": aprobada}


def datos(personas, asignaciones=None, ausencias=None):
    return {"personas": personas, "asignaciones": asignaciones or [],
            "ausencias": ausencias or []}


def test_utilizacion_individual_basica():
    d = datos([persona("P1")], [asg("P1")])
    r = legado.calcular(d, JUL_D, JUL_H)
    assert r["detalle"]["P1"] == 100.0


def test_media_dedicacion_da_media_utilizacion():
    d = datos([persona("P1")], [asg("P1", ded=50)])
    r = legado.calcular(d, JUL_D, JUL_H)
    assert r["detalle"]["P1"] == 50.0


def test_las_vacaciones_reducen_la_capacidad():
    d = datos([persona("P1")], [], [aus("P1", "vacaciones", "2026-07-06", "2026-07-10")])
    assert legado.capacidad("P1", d["ausencias"], JUL_D, JUL_H) == 18


def test_la_formacion_no_reduce_la_capacidad_en_el_legado():
    """El legado coincide aqui con el motor nuevo: la formacion si es capacidad."""
    d = datos([persona("P1")], [], [aus("P1", "formacion", "2026-07-06", "2026-07-10")])
    assert legado.capacidad("P1", d["ausencias"], JUL_D, JUL_H) == 23


def test_comportamiento_no_documentado_1_el_banquillo_se_excluye_del_global():
    """A la gente sin ninguna asignacion se la saca del calculo ENTERA.

    Consecuencia: la utilizacion de la compania sube sin que nadie haya
    trabajado mas. Vino del "ajuste banquillo" de 2021 y no esta escrito en
    ninguna parte del repo heredado.
    """
    d = datos([persona("P1"), persona("P2")], [asg("P1")])
    r = legado.calcular(d, JUL_D, JUL_H)
    # P2 esta en banquillo y desaparece: el global es el 100% de P1
    assert r["utilizacion_global"] == 100.0
    assert r["detalle"]["P2"] == 0.0
    assert r["personas"] == 2


def test_comportamiento_no_documentado_1_caso_extremo():
    """Con 1 persona ocupada y 4 en banquillo, el legado sigue diciendo 100%."""
    personas = [persona("P%d" % i) for i in range(1, 6)]
    d = datos(personas, [asg("P1")])
    r = legado.calcular(d, JUL_D, JUL_H)
    assert r["utilizacion_global"] == 100.0


def test_comportamiento_no_documentado_2_promedia_porcentajes_ya_redondeados():
    """El global promedia utilizaciones individuales redondeadas, en lugar de
    agregar numerador y denominador. Con capacidades distintas, los dos caminos
    dan numeros distintos, y de este sale el cuadro de mando."""
    d = datos([persona("P1"), persona("P2")],
              [asg("P1", ded=50), asg("P2", ded=100)],
              [aus("P2", "vacaciones", "2026-07-06", "2026-07-24")])
    r = legado.calcular(d, JUL_D, JUL_H)
    # P1: 50% sobre 23 dias. P2: asignado los 23 dias pero capacidad 8 -> 287.5%
    assert r["detalle"]["P2"] > 100.0
    assert r["utilizacion_global"] == round((50.0 + r["detalle"]["P2"]) / 2, 2)


def test_comportamiento_no_documentado_2_la_asignacion_computa_en_vacaciones():
    """El legado cuenta como asignados dias que la persona estaba de vacaciones.

    Numerador y denominador no excluyen los mismos dias, asi que la utilizacion
    individual se dispara por encima del 100% sin que nadie haya trabajado mas.
    """
    d = datos([persona("P1")], [asg("P1")],
              [aus("P1", "vacaciones", "2026-07-06", "2026-07-24")])
    r = legado.calcular(d, JUL_D, JUL_H)
    assert r["detalle"]["P1"] == 287.5


def test_la_sobreasignacion_no_se_corta_en_el_legado():
    d = datos([persona("P1")], [asg("P1", ded=100), asg("P1", ded=50)])
    r = legado.calcular(d, JUL_D, JUL_H)
    assert r["detalle"]["P1"] == 150.0


def test_sin_capacidad_devuelve_cero_sin_error():
    d = datos([persona("P1")], [], [aus("P1", "vacaciones", JUL_D, JUL_H)])
    r = legado.calcular(d, JUL_D, JUL_H)
    assert r["detalle"]["P1"] == 0.0


def test_la_cache_es_por_periodo_y_no_por_datos():
    """Comportamiento peligroso: dos conjuntos de datos distintos del mismo mes
    devuelven el primero. Se caracteriza, no se justifica."""
    primero = legado.calcular(datos([persona("P1")], [asg("P1")]), JUL_D, JUL_H)
    segundo = legado.calcular(datos([persona("P1")], [asg("P1", ded=25)]), JUL_D, JUL_H)
    assert primero["utilizacion_global"] == segundo["utilizacion_global"] == 100.0


def test_el_corpus_sintetico_hace_aflorar_los_dos_defectos():
    """Si este test falla, alguien ha tocado el generador o la semilla."""
    corpus = json.loads((RAIZ / "datos" / "corpus_sintetico.json").read_text(encoding="utf-8"))
    assert len(corpus["personas"]) == 180
    legado._CACHE.clear()
    r = legado.calcular(corpus, JUL_D, JUL_H)
    por_encima = [p for p, v in r["detalle"].items() if v > 100.0]
    assert por_encima, "el defecto de asignacion en vacaciones debe aflorar en el corpus"
    assert r["utilizacion_global"] > 0
