# -*- coding: utf-8 -*-
# calculadora_utilizacion_v1.py
# Modulo heredado. Sin tests. Sin documentacion de reglas.
# NO TOCAR sin caracterizar antes: de este numero sale el cuadro de mando
# mensual que ve direccion.
#
# Historico (lo poco que se sabe):
#   2019-05  version inicial, salio de una macro de Excel
#   2021-02  "ajuste banquillo" pedido por operaciones (nadie recuerda quien)
#   2022-09  se anade redondeo por peticion de reporting
#   2024-04  se anade el desglose por pais, sin tocar el calculo
#
# ATENCION para el student: este fichero es el objeto de la estacion S5.
# Antes de refactorizar nada tienes que caracterizarlo. Si empiezas por el
# refactor, el verificador de S5 lo detecta en el historial de git y la
# estacion no se supera.

import json
from datetime import date, timedelta

JORNADA = 8
DEC = 2
NO_TRABAJABLE = ["vacaciones", "festivo", "baja"]
_CACHE = {}
DEBUG = False


def _log(m):
    if DEBUG:
        print("[util] " + str(m))


def parse(f):
    return date.fromisoformat(f) if isinstance(f, str) else f


def laborables(desde, hasta):
    d = parse(desde)
    h = parse(hasta)
    n = 0
    while d <= h:
        if d.weekday() < 5:
            n = n + 1
        d = d + timedelta(days=1)
    return n


def solapan(a1, a2, b1, b2):
    return parse(a1) <= parse(b2) and parse(b1) <= parse(a2)


def ausencias_de(persona, ausencias):
    r = []
    for a in ausencias:
        if a["persona_id"] == persona:
            r.append(a)
    return r


def dias_ausencia(persona, ausencias, desde, hasta):
    total = 0
    for a in ausencias_de(persona, ausencias):
        if a["tipo"] not in NO_TRABAJABLE:
            continue
        if not a.get("aprobada", True):
            continue
        if not solapan(a["desde"], a["hasta"], desde, hasta):
            continue
        d = max(parse(a["desde"]), parse(desde))
        h = min(parse(a["hasta"]), parse(hasta))
        total = total + laborables(d, h)
    return total


def esta_en_banquillo(persona, asignaciones, desde, hasta):
    for a in asignaciones:
        if a["persona_id"] != persona:
            continue
        if solapan(a["desde"], a["hasta"], desde, hasta):
            return False
    return True


def capacidad(persona, ausencias, desde, hasta):
    return laborables(desde, hasta) - dias_ausencia(persona, ausencias, desde, hasta)


def asignados(persona, asignaciones, desde, hasta):
    # COMPORTAMIENTO NO DOCUMENTADO 2 (parte 1)
    # no se corta la dedicacion en el 100%: una persona al 150% aporta 1.5 dias
    # por dia, y eso sube la utilizacion de un equipo sobreasignado.
    total = 0.0
    for a in asignaciones:
        if a["persona_id"] != persona:
            continue
        if not solapan(a["desde"], a["hasta"], desde, hasta):
            continue
        d = max(parse(a["desde"]), parse(desde))
        h = min(parse(a["hasta"]), parse(hasta))
        total = total + laborables(d, h) * (a["dedicacion_pct"] / 100.0)
    return total


def utilizacion_persona(persona, asignaciones, ausencias, desde, hasta):
    cap = capacidad(persona, ausencias, desde, hasta)
    if cap == 0:
        return 0.0
    asg = asignados(persona, asignaciones, desde, hasta)
    return round(asg * 100.0 / cap, DEC)


def utilizacion_global(personas, asignaciones, ausencias, desde, hasta):
    # COMPORTAMIENTO NO DOCUMENTADO 1
    # a la gente en banquillo se la saca del calculo entera, no solo del
    # numerador. La utilizacion de la compania sube sin que nadie trabaje mas.
    # vino del "ajuste banquillo" de 2021.
    #
    # COMPORTAMIENTO NO DOCUMENTADO 2 (parte 2)
    # ademas se promedian utilizaciones ya redondeadas por persona, en lugar de
    # agregar numerador y denominador. de este numero sale el cuadro de mando.
    vals = []
    for p in personas:
        pid = p["persona_id"]
        if esta_en_banquillo(pid, asignaciones, desde, hasta):
            _log("excluido por banquillo: " + pid)
            continue
        if capacidad(pid, ausencias, desde, hasta) == 0:
            continue
        vals.append(utilizacion_persona(pid, asignaciones, ausencias, desde, hasta))
    if len(vals) == 0:
        return 0.0
    s = 0.0
    for v in vals:
        s = s + v
    return round(s / len(vals), DEC)


def calcular(datos, desde, hasta):
    # punto de entrada historico. lo llama el proceso mensual de reporting.
    key = str(desde) + "|" + str(hasta)
    if key in _CACHE:
        _log("cache hit " + key)
        return _CACHE[key]
    res = {}
    res["desde"] = str(desde)
    res["hasta"] = str(hasta)
    res["utilizacion_global"] = utilizacion_global(
        datos["personas"], datos["asignaciones"], datos["ausencias"], desde, hasta)
    detalle = {}
    for p in datos["personas"]:
        detalle[p["persona_id"]] = utilizacion_persona(
            p["persona_id"], datos["asignaciones"], datos["ausencias"], desde, hasta)
    res["detalle"] = detalle
    res["personas"] = len(datos["personas"])
    _CACHE[key] = res
    return res


def por_pais(datos, desde, hasta):
    d = {}
    for p in datos["personas"]:
        pais = p.get("pais", "ND")
        if pais not in d:
            d[pais] = []
        d[pais].append(utilizacion_persona(
            p["persona_id"], datos["asignaciones"], datos["ausencias"], desde, hasta))
    out = {}
    for k in d:
        out[k] = round(sum(d[k]) / len(d[k]), DEC) if d[k] else 0.0
    return out


# --- codigo muerto: quedo de la migracion de 2022, no lo llama nadie ---

def utilizacion_simple(asignaciones):
    s = 0
    for a in asignaciones:
        s = s + a["dedicacion_pct"]
    return round(s / 100.0, DEC)


def formatea(res):
    return "%s;%s;%s" % (res["desde"], res["hasta"], res["utilizacion_global"])


def exporta_csv(res, ruta):
    f = open(ruta, "w", encoding="utf-8")
    f.write(formatea(res) + "\n")
    f.close()
    return ruta
