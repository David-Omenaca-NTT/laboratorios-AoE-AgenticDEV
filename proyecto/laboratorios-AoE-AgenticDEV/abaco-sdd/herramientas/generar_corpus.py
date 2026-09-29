"""Genera el corpus sintetico del repositorio de APRENDIZAJE.

Determinista: misma semilla, mismo corpus. Es requisito, porque el informe de
equivalencia de S5 tiene que ser reproducible por el mentor.

IMPORTANTE: este corpus es sintetico y se queda en el repositorio de
aprendizaje. Los datos reales viven solo en el repositorio de producto y no se
copian aqui bajo ninguna circunstancia.
"""
from __future__ import annotations

import json
import random
from datetime import date, timedelta
from pathlib import Path

SEMILLA = 20260901
N_PERSONAS = 180
RAIZ = Path(__file__).resolve().parents[1]

CATEGORIAS = ["BEC", "JUN", "CON", "SEN", "LEA", "MAN", "DIR"]
PESOS = [8, 22, 30, 25, 8, 5, 2]
SKILLS = ["java", "python", "aws", "azure", "kubernetes", "terraform", "react",
          "angular", "sql", "mulesoft", "sap", "scrum", "testing", "seguridad"]
PAISES = ["ES", "PT", "MX", "CO", "PE"]
OFICINAS = ["Madrid", "Barcelona", "Valencia", "Lisboa", "CDMX", "Bogota", "Lima"]
NOMBRES = ["Persona %03d" % i for i in range(N_PERSONAS)]


def generar(n=N_PERSONAS, semilla=SEMILLA):
    rnd = random.Random(semilla)
    inicio = date(2026, 1, 1)
    personas, ausencias, asignaciones, proyectos = [], [], [], []

    for i in range(n):
        cat = rnd.choices(CATEGORIAS, weights=PESOS)[0]
        alta = inicio - timedelta(days=rnd.randint(60, 2500))
        historico = [{"codigo_categoria": cat, "desde": alta.isoformat(), "hasta": None}]
        # Un 20% ha promocionado: dos vigencias, la anterior cerrada
        if rnd.random() < 0.2 and CATEGORIAS.index(cat) > 0:
            anterior = CATEGORIAS[CATEGORIAS.index(cat) - 1]
            corte = inicio - timedelta(days=rnd.randint(30, 400))
            historico = [
                {"codigo_categoria": anterior, "desde": alta.isoformat(),
                 "hasta": (corte - timedelta(days=1)).isoformat()},
                {"codigo_categoria": cat, "desde": corte.isoformat(), "hasta": None},
            ]
        skills = []
        for s in rnd.sample(SKILLS, rnd.randint(3, 7)):
            skills.append({"codigo": s, "nivel": rnd.choices([1,2,3,4,5], weights=[1,2,3,3,2])[0],
                           "ultimo_uso": (inicio - timedelta(days=rnd.randint(0, 900))).isoformat()})
        personas.append({
            "persona_id": "PER-%04d" % i, "nombre": NOMBRES[i],
            "pais": rnd.choice(PAISES), "oficina": rnd.choice(OFICINAS),
            "fecha_alta": alta.isoformat(), "fecha_baja": None,
            "historico_categoria": historico, "skills": skills})

    for j in range(25):
        d = inicio + timedelta(days=rnd.randint(0, 60))
        proyectos.append({"codigo": "PRY-%03d" % j, "nombre": "Proyecto %03d" % j,
                          "cliente": "Cliente %02d" % rnd.randint(1, 12),
                          "responsable": "PER-%04d" % rnd.randrange(n),
                          "desde": d.isoformat(),
                          "hasta": (d + timedelta(days=rnd.randint(90, 400))).isoformat()})

    for p in personas:
        # 18% en banquillo: sin ninguna asignacion
        if rnd.random() < 0.18:
            continue
        for _ in range(rnd.randint(1, 3)):
            pry = rnd.choice(proyectos)
            d = date.fromisoformat(pry["desde"]) + timedelta(days=rnd.randint(0, 40))
            h = d + timedelta(days=rnd.randint(60, 300))
            asignaciones.append({
                "asignacion_id": "ASG-%s-%s-%s" % (p["persona_id"], pry["codigo"], d.isoformat()),
                "persona_id": p["persona_id"], "proyecto": pry["codigo"],
                "rol": rnd.choice(["desarrollo", "arquitectura", "qa", "gestion"]),
                "desde": d.isoformat(), "hasta": h.isoformat(),
                "dedicacion_pct": rnd.choices([25, 50, 100], weights=[2, 3, 5])[0],
                "modalidad": "porcentual",
                "categoria_registrada": p["historico_categoria"][0]["codigo_categoria"],
                "version_catalogo": "CAT-2026", "version_politica": "POL-2026",
                "confirmada": True, "horas": None})

    for p in personas:
        for _ in range(rnd.randint(0, 3)):
            tipo = rnd.choices(["vacaciones", "formacion", "festivo", "baja", "banquillo"],
                               weights=[5, 3, 2, 1, 2])[0]
            d = inicio + timedelta(days=rnd.randint(0, 300))
            ausencias.append({"persona_id": p["persona_id"], "tipo": tipo,
                              "desde": d.isoformat(),
                              "hasta": (d + timedelta(days=rnd.randint(1, 20))).isoformat(),
                              "aprobada": True})

    return {"personas": personas, "proyectos": proyectos,
            "asignaciones": asignaciones, "ausencias": ausencias}


if __name__ == "__main__":
    datos = generar()
    destino = RAIZ / "datos" / "corpus_sintetico.json"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(json.dumps(datos, ensure_ascii=False), encoding="utf-8")
    print("corpus sintetico: %d personas, %d asignaciones, %d ausencias, %d proyectos"
          % (len(datos["personas"]), len(datos["asignaciones"]),
             len(datos["ausencias"]), len(datos["proyectos"])))
