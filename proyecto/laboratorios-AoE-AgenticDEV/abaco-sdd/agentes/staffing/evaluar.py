"""Evaluacion del agente de staffing contra el conjunto dorado.

Tres metricas separadas, y la separacion es la leccion de la estacion:

  SEGURIDAD   violaciones de restriccion dura. Umbral: 0. Sin tolerancia.
              Proponer a alguien no disponible, por debajo de la categoria
              pedida o sin el nivel de skill exigido. Una sola violacion
              destruye la confianza en el sistema entero.

  UTILIDAD    que la persona que el humano acabo eligiendo este entre las tres
              primeras propuestas. Umbral: 0,70. Un agente seguro pero inutil
              se apaga a la semana.

  CONCENTRACION  cuantas personas distintas aparecen propuestas sobre el pool
              disponible, y su reparto por categoria. Se mide y se declara, sin
              umbral en la cohorte 1.

Promediar seguridad y utilidad en un unico numero seria un error de diseno: son
obligaciones distintas y una no compensa a la otra.

Uso:
    python3 -m agentes.staffing.evaluar
    python3 -m agentes.staffing.evaluar --guardar
"""
from __future__ import annotations

import argparse
import json
import time
from collections import Counter
from datetime import date
from pathlib import Path

from .agente import RAIZ, cargar_contexto, proponer


def violaciones_de_restriccion(propuesta, contexto: dict, restricciones: dict,
                               desde: date, hasta: date) -> list:
    """Recomprueba las restricciones duras contra los candidatos propuestos.

    Es una verificacion independiente del propio agente: si el agente se
    equivoca en su filtrado, esto lo detecta. No se confia en que el agente
    diga que ha filtrado bien.
    """
    from abaco.reglas.motor import evaluar_candidato
    from abaco.reglas.politicas import cargar_politica, catalogo_vigente_en
    from abaco.dominio.modelos import Posicion

    catalogo = catalogo_vigente_en(desde, RAIZ / "politicas" / "categorias")
    politica = cargar_politica("POL-2026", RAIZ / "politicas" / "capacidad")
    personas = {p.persona_id: p for p in contexto["personas"]}
    fallos = []

    for bloque in propuesta.posiciones:
        # La recomprobacion tiene que usar EXACTAMENTE los mismos parametros que
        # la propuesta. Con una dedicacion fija distinta de la pedida, el
        # verificador produce falsos positivos de sobreasignacion y acusa al
        # agente de algo que no ha hecho.
        posicion = Posicion(rol=bloque.rol, codigo_categoria=bloque.categoria_pedida,
                            skill=bloque.skill_pedido, nivel_minimo=bloque.nivel_minimo,
                            dedicacion_pct=bloque.dedicacion_pct)
        for c in bloque.candidatos:
            persona = personas.get(c.persona_id)
            if persona is None:
                fallos.append({"persona": c.persona_id, "motivo": "persona inexistente"})
                continue
            v = evaluar_candidato(persona, posicion, desde, hasta, catalogo, politica,
                                  contexto["asignaciones"], contexto["ausencias"])
            if not v.apta:
                fallos.append({"persona": c.persona_id, "motivo": "; ".join(v.motivos)})
    return fallos


def ejecutar(directorio: Path, contexto: dict, motor=proponer, maximo: int = 3) -> dict:
    etiquetas = json.loads((directorio / "etiquetas.json").read_text(encoding="utf-8"))

    violaciones, detalle, latencias = [], [], []
    aciertos_top = evaluables = 0
    propuestos = Counter()
    propuestos_por_categoria = Counter()

    for ident, etiqueta in sorted(etiquetas.items()):
        demanda = json.loads((directorio / ("%s.json" % ident)).read_text(encoding="utf-8"))
        desde = date.fromisoformat(demanda["desde"])
        hasta = date.fromisoformat(demanda["hasta"])

        t0 = time.perf_counter()
        propuesta = motor(demanda, contexto, maximo=maximo)
        latencias.append((time.perf_counter() - t0) * 1000)

        fallos = violaciones_de_restriccion(propuesta, contexto,
                                            etiqueta["restricciones"], desde, hasta)
        for f in fallos:
            violaciones.append({"caso": ident, **f})

        candidatos = [c.persona_id for b in propuesta.posiciones for c in b.candidatos]
        for b in propuesta.posiciones:
            for c in b.candidatos:
                propuestos[c.persona_id] += 1
                propuestos_por_categoria[c.categoria_registrada] += 1

        if etiqueta["sin_candidatos"]:
            resultado = "sin candidatos, correcto" if not candidatos else "propone donde no debia"
            if candidatos:
                violaciones.append({"caso": ident, "persona": candidatos[0],
                                    "motivo": "el conjunto dorado declara que no habia candidatos validos"})
        else:
            evaluables += 1
            acierto = etiqueta["elegido"] in candidatos[:maximo]
            aciertos_top += 1 if acierto else 0
            resultado = "acierto" if acierto else "la eleccion humana no esta en el top %d" % maximo
        detalle.append({"caso": ident, "esperado": etiqueta["elegido"],
                        "propuestos": candidatos[:maximo], "resultado": resultado})

    pool = len(contexto["personas"])
    personas_distintas = len(propuestos)
    top5 = propuestos.most_common(5)
    cuota_top5 = (sum(n for _, n in top5) / sum(propuestos.values())) if propuestos else 0.0

    return {
        "fecha": date.today().isoformat(),
        "casos": len(etiquetas),
        "seguridad": {
            "violaciones": len(violaciones),
            "umbral": 0,
            "supera": len(violaciones) == 0,
            "detalle": violaciones[:10],
        },
        "utilidad": {
            "casos_evaluables": evaluables,
            "aciertos_top_%d" % maximo: aciertos_top,
            "ratio": round(aciertos_top / evaluables, 3) if evaluables else 0.0,
            "umbral": 0.70,
            "supera": (aciertos_top / evaluables if evaluables else 0) >= 0.70,
        },
        "concentracion": {
            "pool": pool,
            "personas_distintas_propuestas": personas_distintas,
            "cobertura_del_pool": round(personas_distintas / pool, 3) if pool else 0.0,
            "cuota_de_los_5_mas_propuestos": round(cuota_top5, 3),
            "top5": top5,
            "reparto_por_categoria": dict(propuestos_por_categoria),
        },
        "latencia_media_ms": round(sum(latencias) / len(latencias), 1) if latencias else 0.0,
        "coste_usd_por_ejecucion": 0.0,
        "juez": "offline",
        "detalle": detalle,
    }


def principal(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dorado", default="evals/dorado_ejemplo")
    ap.add_argument("--guardar", action="store_true")
    ap.add_argument("--v0", action="store_true", help="evalua la linea base ingenua")
    args = ap.parse_args(argv)

    contexto = cargar_contexto()
    motor = proponer
    if args.v0:
        from .agente_v0 import proponer_v0
        motor = proponer_v0

    informe = ejecutar(RAIZ / args.dorado, contexto, motor=motor)
    informe["version_agente"] = "v0 linea base" if args.v0 else "final"
    resumen = {k: v for k, v in informe.items() if k != "detalle"}
    resumen["seguridad"] = {k: v for k, v in resumen["seguridad"].items() if k != "detalle"}
    print(json.dumps(resumen, ensure_ascii=False, indent=2))

    if informe["seguridad"]["violaciones"]:
        print("\nViolaciones de restriccion dura (las primeras):")
        for v in informe["seguridad"]["detalle"][:5]:
            print("  %s -> %s: %s" % (v["caso"], v["persona"], v["motivo"]))

    if args.guardar:
        destino = RAIZ / "evals" / "informes"
        destino.mkdir(parents=True, exist_ok=True)
        nombre = "evaluacion-%s-%s.json" % ("v0" if args.v0 else "final",
                                            time.strftime("%Y%m%d-%H%M%S"))
        (destino / nombre).write_text(json.dumps(informe, ensure_ascii=False, indent=2),
                                      encoding="utf-8")
        print("\ninforme guardado en evals/informes/%s" % nombre)

    ok = informe["seguridad"]["supera"] and informe["utilidad"]["supera"]
    print("\numbrales de S4a: %s" % ("SUPERADOS" if ok else "NO SUPERADOS"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(principal())
