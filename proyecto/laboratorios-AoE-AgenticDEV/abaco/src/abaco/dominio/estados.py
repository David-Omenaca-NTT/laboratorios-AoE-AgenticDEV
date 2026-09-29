"""Maquina de estados de la demanda. Implementa SPEC-003.

Los ocho estados salen del PRD tal cual. El invariante que importa: una demanda
cerrada o cancelada no admite asignaciones nuevas.
"""
from __future__ import annotations

from .modelos import Demanda, EstadoDemanda

E = EstadoDemanda

TRANSICIONES = {
    E.SOLICITADA: {E.APROBADA, E.CANCELADA},
    E.APROBADA: {E.BUSCANDO, E.CANCELADA},
    E.BUSCANDO: {E.CANDIDATO_PROPUESTO, E.CANCELADA},
    E.CANDIDATO_PROPUESTO: {E.ACEPTADA, E.BUSCANDO, E.CANCELADA},
    E.ACEPTADA: {E.ASIGNADA, E.BUSCANDO, E.CANCELADA},
    E.ASIGNADA: {E.CERRADA},
    E.CERRADA: set(),
    E.CANCELADA: set(),
}

ESTADOS_TERMINALES = {E.CERRADA, E.CANCELADA}


class TransicionInvalida(Exception):
    pass


class DemandaTerminada(Exception):
    pass


def transiciones_validas(estado: EstadoDemanda) -> set:
    return TRANSICIONES[estado]


def transicionar(demanda: Demanda, destino: EstadoDemanda) -> Demanda:
    if destino not in TRANSICIONES[demanda.estado]:
        raise TransicionInvalida(
            "no se puede pasar de %s a %s" % (demanda.estado.value, destino.value))
    demanda.estado = destino
    return demanda


def admite_asignacion(demanda: Demanda) -> bool:
    """SPEC-003/INV-01: una demanda terminal no admite asignaciones nuevas."""
    return demanda.estado not in ESTADOS_TERMINALES


def exigir_admite_asignacion(demanda: Demanda) -> None:
    if not admite_asignacion(demanda):
        raise DemandaTerminada(
            "la demanda %s esta en estado %s y no admite asignaciones"
            % (demanda.demanda_id, demanda.estado.value))


def devuelta_a_busqueda(demanda: Demanda) -> Demanda:
    """SPEC-003/CA-04: un candidato rechazado devuelve la demanda a busqueda,
    no la cancela ni la deja bloqueada."""
    if demanda.estado not in (E.CANDIDATO_PROPUESTO, E.ACEPTADA):
        raise TransicionInvalida(
            "solo se vuelve a busqueda desde candidato propuesto o aceptada")
    demanda.estado = E.BUSCANDO
    return demanda
