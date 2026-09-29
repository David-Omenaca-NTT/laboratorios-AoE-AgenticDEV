"""Constructores de datos para los tests. Sin logica de negocio aqui."""
from datetime import date
from pathlib import Path

from abaco.dominio.modelos import (Ausencia, Asignacion, CategoriaVigencia,
                                   Demanda, Modalidad, Persona, Posicion,
                                   Skill, TipoDisponibilidad)
from abaco.reglas.politicas import cargar_catalogo, cargar_politica

RAIZ = Path(__file__).resolve().parents[1]


def catalogo(version="CAT-2026"):
    return cargar_catalogo(version, RAIZ / "politicas" / "categorias")


def politica(version="POL-2026"):
    return cargar_politica(version, RAIZ / "politicas" / "capacidad")


def persona(pid="PER-0001", categoria="SEN", desde=date(2020, 1, 1),
            skills=None, alta=date(2020, 1, 1), baja=None, historico=None):
    return Persona(
        persona_id=pid, nombre="Persona de prueba", pais="ES", oficina="Valencia",
        fecha_alta=alta, fecha_baja=baja,
        historico_categoria=historico or [CategoriaVigencia(categoria, desde)],
        skills=skills or [Skill("java", 4, date(2025, 6, 1))])


def posicion(rol="desarrollo", categoria="SEN", skill="java", nivel=4, ded=100):
    return Posicion(rol=rol, codigo_categoria=categoria, skill=skill,
                    nivel_minimo=nivel, dedicacion_pct=ded)


def asignacion(pid="PER-0001", proyecto="PRY-001", desde=date(2026, 3, 1),
               hasta=date(2026, 6, 30), ded=100, rol="desarrollo",
               categoria="SEN", confirmada=False):
    return Asignacion(
        asignacion_id="ASG-%s-%s-%s" % (pid, proyecto, desde.isoformat()),
        persona_id=pid, proyecto=proyecto, rol=rol, desde=desde, hasta=hasta,
        dedicacion_pct=ded, modalidad=Modalidad.PORCENTUAL,
        categoria_registrada=categoria, version_catalogo="CAT-2026",
        version_politica="POL-2026", confirmada=confirmada)


def ausencia(pid="PER-0001", tipo="vacaciones", desde=date(2026, 8, 1),
             hasta=date(2026, 8, 20), aprobada=True):
    return Ausencia(persona_id=pid, tipo=TipoDisponibilidad(tipo),
                    desde=desde, hasta=hasta, aprobada=aprobada)


def demanda(did="DEM-001", posiciones=None, desde=date(2026, 7, 1),
            hasta=date(2026, 12, 31), prioridad="alta",
            momento="2026-05-10T09:00:00"):
    return Demanda(demanda_id=did, proyecto="PRY-001", solicitante="PER-0100",
                   posiciones=posiciones or [posicion()], desde=desde, hasta=hasta,
                   prioridad=prioridad, momento_solicitud=momento)
