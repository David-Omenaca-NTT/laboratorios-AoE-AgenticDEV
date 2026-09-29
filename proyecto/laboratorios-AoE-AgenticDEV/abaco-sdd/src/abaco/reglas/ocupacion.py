# GENERADO DESDE ESPECIFICACION. NO EDITAR A MANO.
# Capability: ocupacion
# Cambio de origen: e5-ocupacion-utilizacion
# Si algo esta mal aqui, esta mal en la spec. Corrige la spec y regenera.
"""Utilizacion y ocupacion. Implementa SPEC-002.

Aqui vive el invariante numerico del proyecto:

  El redondeo se aplica UNA sola vez y AL FINAL. Nunca por persona ni por mes
  antes de agregar. Cualquier redondeo intermedio mueve la utilizacion agregada,
  y de ese numero cuelga la conversacion de desempeno de gente con nombre.

Resolucion de la ambiguedad de SPEC-002 (ver apartado de ambiguedades):

  A-01, denominador: la formacion y el banquillo SI entran en la capacidad
  disponible. Excluirlos sube la utilizacion de la compania sin que nadie haya
  trabajado mas, que es exactamente lo que hace el sistema heredado. Solo se
  excluyen del denominador las ausencias no trabajables: vacaciones, festivos y
  bajas.

  A-02, numerador: una sobreasignacion se corta en el 100% al agregar. Un equipo
  al 120% no es un equipo eficiente, es un equipo quemado, y dejar que aporte 120
  premia justo lo que hay que vigilar. La sobreasignacion se reporta como
  indicador propio, no diluida dentro de la utilizacion.
"""
from __future__ import annotations

from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal

from ..dominio.modelos import CatalogoCategorias, Persona, TipoDisponibilidad

DOS_DECIMALES = Decimal("0.01")

# A-01: tipos que NO computan como capacidad disponible
NO_TRABAJABLES = {TipoDisponibilidad.VACACIONES, TipoDisponibilidad.FESTIVO,
                  TipoDisponibilidad.BAJA}


def _redondear(valor: Decimal) -> Decimal:
    return valor.quantize(DOS_DECIMALES, rounding=ROUND_HALF_UP)


def dias_laborables(desde: date, hasta: date) -> int:
    """Dias laborables del intervalo, ambos inclusive. Lunes a viernes."""
    total = 0
    actual = desde
    while actual <= hasta:
        if actual.weekday() < 5:
            total += 1
        actual += timedelta(days=1)
    return total


def dias_no_trabajables(persona_id: str, ausencias: list,
                        desde: date, hasta: date) -> int:
    """Dias laborables cubiertos por ausencia no trabajable aprobada."""
    dias = set()
    for a in ausencias:
        if a.persona_id != persona_id or not a.aprobada:
            continue
        if a.tipo not in NO_TRABAJABLES:
            continue
        actual = max(a.desde, desde)
        fin = min(a.hasta, hasta)
        while actual <= fin:
            if actual.weekday() < 5:
                dias.add(actual)
            actual += timedelta(days=1)
    return len(dias)


def capacidad_disponible(persona: Persona, ausencias: list,
                         desde: date, hasta: date) -> int:
    """SPEC-002/CA-01: dias laborables menos ausencias no trabajables.

    Formacion y banquillo NO se restan: son capacidad que existe y no se
    facturo. Esa es la resolucion A-01 y es lo contrario de lo que hace el
    modulo heredado.
    """
    if not persona.activa_en(desde) and not persona.activa_en(hasta):
        return 0
    inicio = max(desde, persona.fecha_alta)
    fin = min(hasta, persona.fecha_baja) if persona.fecha_baja else hasta
    if inicio > fin:
        return 0
    return dias_laborables(inicio, fin) - dias_no_trabajables(
        persona.persona_id, ausencias, inicio, fin)


def _dias_excluidos(persona_id: str, ausencias: list,
                    desde: date, hasta: date) -> set:
    """Dias laborables cubiertos por ausencia no trabajable aprobada."""
    excluidos = set()
    for a in ausencias or []:
        if a.persona_id != persona_id or not a.aprobada:
            continue
        if a.tipo not in NO_TRABAJABLES:
            continue
        actual = max(a.desde, desde)
        fin = min(a.hasta, hasta)
        while actual <= fin:
            if actual.weekday() < 5:
                excluidos.add(actual)
            actual += timedelta(days=1)
    return excluidos


def dias_asignados(persona_id: str, asignaciones: list, desde: date, hasta: date,
                   ausencias: list = None, cortar_en_100: bool = True) -> Decimal:
    """Dias equivalentes asignados, ponderados por dedicacion.

    SPEC-002/CA-03: el prorrateo es por dias laborables efectivos del solape,
    no por dias naturales ni por mes completo.
    SPEC-002/CA-05: con cortar_en_100, la suma de dedicaciones se corta al 100%
    en cada dia (resolucion A-02).
    SPEC-002/CA-08: una asignacion no computa durante una ausencia no
    trabajable. Alguien asignado al 100% que esta tres semanas de vacaciones no
    ha trabajado esas tres semanas, y contarlas dispara su utilizacion por
    encima del 100% sin que nadie haya hecho nada.

    Numerador y denominador tienen que excluir exactamente los mismos dias. Si
    no, el cociente no significa nada.
    """
    excluidos = _dias_excluidos(persona_id, ausencias, desde, hasta)
    total = Decimal("0")
    actual = desde
    while actual <= hasta:
        if actual.weekday() < 5 and actual not in excluidos:
            pct = sum(a.dedicacion_pct for a in asignaciones
                      if a.persona_id == persona_id and a.desde <= actual <= a.hasta)
            total += Decimal(min(pct, 100) if cortar_en_100 else pct) / Decimal(100)
        actual += timedelta(days=1)
    return total


def utilizacion(persona: Persona, asignaciones: list, ausencias: list,
                desde: date, hasta: date) -> Decimal:
    """SPEC-002/CA-01, CA-03, CA-05. Porcentaje con dos decimales.

    Sin capacidad disponible devuelve 0,00 sin error.
    """
    capacidad = capacidad_disponible(persona, ausencias, desde, hasta)
    if capacidad == 0:
        return _redondear(Decimal("0"))
    asignados = dias_asignados(persona.persona_id, asignaciones, desde, hasta,
                               ausencias)
    return _redondear(asignados / Decimal(capacidad) * Decimal(100))


def sobreasignacion(persona: Persona, asignaciones: list,
                    desde: date, hasta: date) -> Decimal:
    """SPEC-002/CA-06: la sobreasignacion se reporta aparte, no diluida.

    Dias equivalentes por encima del 100%, sobre la capacidad del periodo.
    """
    exceso = Decimal("0")
    actual = desde
    while actual <= hasta:
        if actual.weekday() < 5:
            pct = sum(a.dedicacion_pct for a in asignaciones
                      if a.persona_id == persona.persona_id and a.desde <= actual <= a.hasta)
            if pct > 100:
                exceso += Decimal(pct - 100) / Decimal(100)
        actual += timedelta(days=1)
    laborables = dias_laborables(desde, hasta)
    if laborables == 0:
        return _redondear(Decimal("0"))
    return _redondear(exceso / Decimal(laborables) * Decimal(100))


def desviacion_sobre_objetivo(persona: Persona, catalogo: CatalogoCategorias,
                              asignaciones: list, ausencias: list,
                              desde: date, hasta: date) -> Decimal:
    """SPEC-002/CA-02: la utilizacion se compara contra el objetivo de la
    categoria de la persona, nunca contra un objetivo unico de compania."""
    codigo = persona.categoria_en(desde)
    if codigo is None:
        return _redondear(Decimal("0"))
    objetivo = catalogo.categoria(codigo).utilizacion_objetivo
    return _redondear(utilizacion(persona, asignaciones, ausencias, desde, hasta)
                      - Decimal(objetivo))


def utilizacion_agregada(personas: list, asignaciones: list, ausencias: list,
                         desde: date, hasta: date) -> Decimal:
    """SPEC-002/INV-01: se agregan numerador y denominador y se redondea UNA vez.

    No se promedian utilizaciones individuales ya redondeadas. Es la diferencia
    con el modulo heredado y es la que mueve el numero de compania.
    """
    numerador = Decimal("0")
    denominador = 0
    for persona in personas:
        capacidad = capacidad_disponible(persona, ausencias, desde, hasta)
        if capacidad == 0:
            continue
        numerador += dias_asignados(persona.persona_id, asignaciones, desde,
                                    hasta, ausencias)
        denominador += capacidad
    if denominador == 0:
        return _redondear(Decimal("0"))
    return _redondear(numerador / Decimal(denominador) * Decimal(100))


def cobertura_demanda(demanda, asignaciones: list, personas: dict,
                      catalogo: CatalogoCategorias) -> Decimal:
    """SPEC-002/CA-04: proporcion de posiciones cubiertas con categoria igual o
    superior a la pedida."""
    if demanda.posiciones_totales == 0:
        return _redondear(Decimal("0"))
    cubiertas = 0
    usadas = set()
    for posicion in demanda.posiciones:
        for a in asignaciones:
            if a.asignacion_id in usadas or a.proyecto != demanda.proyecto:
                continue
            if a.rol != posicion.rol:
                continue
            try:
                suya = catalogo.categoria(a.categoria_registrada)
                pedida = catalogo.categoria(posicion.codigo_categoria)
            except KeyError:
                continue
            if suya.cumple(pedida):
                cubiertas += 1
                usadas.add(a.asignacion_id)
                break
    return _redondear(Decimal(cubiertas) / Decimal(demanda.posiciones_totales) * Decimal(100))


def en_banquillo(persona: Persona, asignaciones: list, ausencias: list,
                 desde: date, hasta: date) -> bool:
    """Sin ninguna asignacion en el periodo y con capacidad disponible."""
    if capacidad_disponible(persona, ausencias, desde, hasta) == 0:
        return False
    return not any(a.persona_id == persona.persona_id and a.solapa(desde, hasta)
                   for a in asignaciones)
