"""BATERIA DE ACEPTACION EXTERNA. ESCRITA A MANO.

Esta carpeta es el unico punto de control fuera del bucle de generacion. Ningun
agente puede escribir aqui: esta en la lista de rutas denegadas del contrato de
contexto, en CODEOWNERS y en el gate de aceptacion del pipeline.

Si el agente pudiera modificar el examen que lo evalua, no habria evaluacion.

Cada test referencia el escenario de la spec que comprueba, con la etiqueta
`escenario:`, y esa referencia es lo que permite auditar que la bateria cubre
de verdad lo que dice cubrir.
"""
import pytest

from abaco.dominio.estados import (DemandaTerminada, TransicionInvalida,
                                   admite_asignacion, devuelta_a_busqueda,
                                   exigir_admite_asignacion, transicionar,
                                   transiciones_validas)
from abaco.dominio.modelos import EstadoDemanda as E
from utilidades import demanda


def test_el_camino_feliz_recorre_los_ocho_estados():
    """cubre: SPEC-003/CA-01"""
    d = demanda()
    for destino in (E.APROBADA, E.BUSCANDO, E.CANDIDATO_PROPUESTO, E.ACEPTADA,
                    E.ASIGNADA, E.CERRADA):
        transicionar(d, destino)
    assert d.estado is E.CERRADA


def test_una_transicion_no_declarada_se_rechaza():
    """cubre: SPEC-003/CA-02"""
    d = demanda()
    with pytest.raises(TransicionInvalida):
        transicionar(d, E.ASIGNADA)


def test_se_puede_cancelar_desde_cualquier_estado_no_terminal():
    """cubre: SPEC-003/CA-03"""
    for estado in (E.SOLICITADA, E.APROBADA, E.BUSCANDO, E.CANDIDATO_PROPUESTO,
                   E.ACEPTADA):
        assert E.CANCELADA in transiciones_validas(estado)


def test_una_demanda_asignada_ya_no_se_cancela():
    """cubre: SPEC-003/CA-03"""
    assert E.CANCELADA not in transiciones_validas(E.ASIGNADA)


def test_un_candidato_rechazado_devuelve_la_demanda_a_busqueda():
    """cubre: SPEC-003/CA-04"""
    d = demanda()
    transicionar(d, E.APROBADA)
    transicionar(d, E.BUSCANDO)
    transicionar(d, E.CANDIDATO_PROPUESTO)
    devuelta_a_busqueda(d)
    assert d.estado is E.BUSCANDO


def test_no_se_vuelve_a_busqueda_desde_un_estado_que_no_lo_admite():
    """cubre: SPEC-003/CA-04"""
    d = demanda()
    with pytest.raises(TransicionInvalida):
        devuelta_a_busqueda(d)


def test_una_demanda_cerrada_o_cancelada_no_admite_asignaciones():
    """cubre: SPEC-003/INV-01"""
    d = demanda()
    transicionar(d, E.CANCELADA)
    assert admite_asignacion(d) is False
    with pytest.raises(DemandaTerminada):
        exigir_admite_asignacion(d)


def test_una_demanda_en_curso_si_admite_asignaciones():
    """cubre: SPEC-003/INV-01"""
    d = demanda()
    transicionar(d, E.APROBADA)
    assert admite_asignacion(d) is True
    exigir_admite_asignacion(d)


def test_los_estados_terminales_no_tienen_salida():
    """cubre: SPEC-003/INV-02"""
    assert transiciones_validas(E.CERRADA) == set()
    assert transiciones_validas(E.CANCELADA) == set()
