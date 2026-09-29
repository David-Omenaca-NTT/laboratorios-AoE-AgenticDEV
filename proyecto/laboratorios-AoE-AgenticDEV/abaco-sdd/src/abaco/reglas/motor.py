# GENERADO DESDE ESPECIFICACION. NO EDITAR A MANO.
# Capability: asignacion
# Cambio de origen: e4-motor-asignacion
# Si algo esta mal aqui, esta mal en la spec. Corrige la spec y regenera.
"""Motor de asignacion. Implementa SPEC-001.

Cada regla lleva en el docstring el identificador del criterio de aceptacion que
la origina, y ese mismo identificador aparece en el test que la cubre. La
trazabilidad la comprueba el verificador de S2.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from typing import Optional

from ..auditoria import registrar_decision
from ..dominio.modelos import (Asignacion, CatalogoCategorias, Modalidad,
                               Persona, Posicion)


class MotivoRechazo:
    NO_ACTIVA = "persona no activa en el periodo"
    SIN_CATEGORIA = "la persona no tiene categoria vigente en la fecha de inicio"
    CATEGORIA_INSUFICIENTE = "categoria por debajo de la pedida"
    SKILL_AUSENTE = "no tiene el skill pedido"
    NIVEL_INSUFICIENTE = "nivel de skill por debajo del minimo"
    AUSENCIA = "ausencia aprobada solapada"
    CAPACIDAD = "supera el 100% de capacidad en el periodo"
    SOBREASIGNACION = "sobreasignacion no aprobada"


@dataclass(frozen=True)
class Politica:
    """Politica de capacidad, versionada. Es configuracion, no codigo."""
    version: str
    tolerancia_sobreasignacion_pct: int      # margen admitido con aprobacion
    permite_sobreasignacion: bool
    dedicaciones_validas: tuple = (25, 50, 100)


@dataclass
class Veredicto:
    apta: bool
    motivos: list


def solapa(a_desde: date, a_hasta: date, b_desde: date, b_hasta: date) -> bool:
    """Solape de intervalos cerrados. Comprobar solo la fecha de inicio es el
    error clasico, y es uno de los defectos de la ronda adversarial R2."""
    return a_desde <= b_hasta and b_desde <= a_hasta


def dedicacion_ocupada(asignaciones: list, persona_id: str,
                       desde: date, hasta: date) -> int:
    """Suma de dedicacion de una persona en cualquier punto solapado."""
    return sum(a.dedicacion_pct for a in asignaciones
               if a.persona_id == persona_id and a.solapa(desde, hasta))


def evaluar_candidato(persona: Persona, posicion: Posicion, desde: date, hasta: date,
                      catalogo: CatalogoCategorias, politica: Politica,
                      asignaciones: list, ausencias: list,
                      sobreasignacion_aprobada: bool = False) -> Veredicto:
    """Aplica todas las restricciones duras de SPEC-001 a un candidato.

    Cubre CA-01, CA-02, CA-03, CA-04 y CA-05. Devuelve el veredicto con TODOS
    los motivos, no solo el primero: el agente necesita poder explicar por que
    descarta a alguien, y un unico motivo da explicaciones pobres.
    """
    motivos = []

    if not persona.activa_en(desde) or not persona.activa_en(hasta):
        motivos.append(MotivoRechazo.NO_ACTIVA)

    # CA-05: la categoria que cuenta es la vigente en la fecha de INICIO
    codigo_categoria = persona.categoria_en(desde)
    if codigo_categoria is None:
        motivos.append(MotivoRechazo.SIN_CATEGORIA)
    else:
        # CA-03: categoria igual o superior a la pedida
        try:
            suya = catalogo.categoria(codigo_categoria)
            pedida = catalogo.categoria(posicion.codigo_categoria)
            if not suya.cumple(pedida):
                motivos.append(MotivoRechazo.CATEGORIA_INSUFICIENTE)
        except KeyError:
            motivos.append(MotivoRechazo.SIN_CATEGORIA)

    # CA-03: skill y nivel minimo
    skill = persona.skill(posicion.skill)
    if skill is None:
        motivos.append(MotivoRechazo.SKILL_AUSENTE)
    elif skill.nivel < posicion.nivel_minimo:
        motivos.append(MotivoRechazo.NIVEL_INSUFICIENTE)

    # CA-04: ausencias aprobadas
    if any(a.persona_id == persona.persona_id and a.aprobada and a.solapa(desde, hasta)
           for a in ausencias):
        motivos.append(MotivoRechazo.AUSENCIA)

    # CA-01 y CA-02: capacidad y sobreasignacion
    ocupada = dedicacion_ocupada(asignaciones, persona.persona_id, desde, hasta)
    total = ocupada + posicion.dedicacion_pct
    if total > 100:
        if not politica.permite_sobreasignacion:
            motivos.append(MotivoRechazo.CAPACIDAD)
        elif total > 100 + politica.tolerancia_sobreasignacion_pct:
            motivos.append(MotivoRechazo.CAPACIDAD)
        elif not sobreasignacion_aprobada:
            motivos.append(MotivoRechazo.SOBREASIGNACION)

    return Veredicto(apta=not motivos, motivos=motivos)


def crear_asignacion(persona: Persona, posicion: Posicion, proyecto: str,
                     desde: date, hasta: date, catalogo: CatalogoCategorias,
                     politica: Politica, asignaciones: list, ausencias: list,
                     actor: str, origen: str = "api",
                     modalidad: Modalidad = Modalidad.PORCENTUAL,
                     horas: Optional[int] = None,
                     sobreasignacion_aprobada: bool = False) -> Asignacion:
    """Crea la asignacion si el candidato es apto. Siempre escribe traza.

    CA-06: la dedicacion debe ser una de las validas de la politica, salvo en
    modalidad horaria.
    INV-01: se registra la version de politica y de catalogo aplicadas.
    """
    veredicto = evaluar_candidato(persona, posicion, desde, hasta, catalogo,
                                  politica, asignaciones, ausencias,
                                  sobreasignacion_aprobada)
    if not veredicto.apta:
        raise ValueError("candidato no apto: %s" % "; ".join(veredicto.motivos))

    if modalidad is Modalidad.PORCENTUAL and \
            posicion.dedicacion_pct not in politica.dedicaciones_validas:
        raise ValueError("dedicacion %d%% no permitida por la politica %s"
                         % (posicion.dedicacion_pct, politica.version))

    asignacion = Asignacion(
        asignacion_id="ASG-%s-%s-%s" % (persona.persona_id, proyecto, desde.isoformat()),
        persona_id=persona.persona_id,
        proyecto=proyecto,
        rol=posicion.rol,
        desde=desde,
        hasta=hasta,
        dedicacion_pct=posicion.dedicacion_pct,
        modalidad=modalidad,
        categoria_registrada=persona.categoria_en(desde),
        version_catalogo=catalogo.version,
        version_politica=politica.version,
        horas=horas,
    )
    registrar_decision(
        entidad="asignacion", entidad_id=asignacion.asignacion_id,
        accion="crear", actor=actor, origen=origen,
        version_politica=politica.version, version_catalogo=catalogo.version,
        momento=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        detalle={"persona": persona.persona_id, "proyecto": proyecto,
                 "rol": posicion.rol, "dedicacion": posicion.dedicacion_pct,
                 "categoria_registrada": asignacion.categoria_registrada},
    )
    return asignacion


def confirmar(asignacion: Asignacion, actor: str, origen: str = "api") -> Asignacion:
    asignacion.confirmada = True
    registrar_decision(
        entidad="asignacion", entidad_id=asignacion.asignacion_id,
        accion="confirmar", actor=actor, origen=origen,
        version_politica=asignacion.version_politica,
        version_catalogo=asignacion.version_catalogo,
        momento=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        detalle={"categoria_registrada": asignacion.categoria_registrada})
    return asignacion


class CategoriaInmutable(Exception):
    pass


def recategorizar(asignacion: Asignacion, nueva_categoria: str, actor: str,
                  nueva_version_catalogo: str, origen: str = "api") -> Asignacion:
    """INV-02: una asignacion confirmada no cambia de categoria en silencio.

    Exige version de catalogo nueva y deja traza. Es la barrera que impide que
    una promocion reescriba el historico.
    """
    if asignacion.confirmada and nueva_version_catalogo == asignacion.version_catalogo:
        raise CategoriaInmutable(
            "la asignacion %s esta confirmada: cambiar la categoria exige una "
            "version de catalogo nueva y queda auditado" % asignacion.asignacion_id)
    anterior = asignacion.categoria_registrada
    asignacion.categoria_registrada = nueva_categoria
    asignacion.version_catalogo = nueva_version_catalogo
    registrar_decision(
        entidad="asignacion", entidad_id=asignacion.asignacion_id,
        accion="recategorizar", actor=actor, origen=origen,
        version_politica=asignacion.version_politica,
        version_catalogo=nueva_version_catalogo,
        momento=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        detalle={"anterior": anterior, "nueva": nueva_categoria})
    return asignacion


def ordenar_demandas(demandas: list) -> list:
    """CA-07: por prioridad declarada y, a igualdad, por fecha de solicitud."""
    peso = {"alta": 0, "media": 1, "baja": 2}
    return sorted(demandas, key=lambda d: (peso.get(d.prioridad, 9), d.momento_solicitud))
