"""BATERIA DE ACEPTACION EXTERNA. ESCRITA A MANO.

Esta carpeta es el unico punto de control fuera del bucle de generacion. Ningun
agente puede escribir aqui: esta en la lista de rutas denegadas del contrato de
contexto, en CODEOWNERS y en el gate de aceptacion del pipeline.

Si el agente pudiera modificar el examen que lo evalua, no habria evaluacion.

Cada test referencia el escenario de la spec que comprueba, con la etiqueta
`escenario:`, y esa referencia es lo que permite auditar que la bateria cubre
de verdad lo que dice cubrir.
"""
import tempfile
from datetime import date
from pathlib import Path

import pytest

from abaco.dominio.modelos import CategoriaVigencia, Modalidad, Skill
from abaco.reglas.motor import (CategoriaInmutable, MotivoRechazo,
                                confirmar, crear_asignacion, dedicacion_ocupada,
                                evaluar_candidato, ordenar_demandas,
                                recategorizar, solapa)
from utilidades import (asignacion, ausencia, catalogo, demanda, persona,
                        politica, posicion)

DESDE = date(2026, 7, 1)
HASTA = date(2026, 12, 31)


@pytest.fixture(autouse=True)
def traza_temporal(monkeypatch):
    import abaco.auditoria as auditoria
    tmp = Path(tempfile.mkdtemp()) / "auditoria.jsonl"
    monkeypatch.setattr(auditoria, "RUTA_TRAZA", tmp)
    yield tmp


def test_sin_asignaciones_previas_el_candidato_es_apto():
    """cubre: SPEC-001/CA-01"""
    v = evaluar_candidato(persona(), posicion(), DESDE, HASTA, catalogo(),
                          politica(), [], [])
    assert v.apta is True
    assert v.motivos == []


def test_no_se_puede_superar_el_100_por_ciento_en_periodo_solapado():
    """cubre: SPEC-001/CA-01"""
    previas = [asignacion(desde=date(2026, 6, 1), hasta=date(2026, 9, 30), ded=100)]
    v = evaluar_candidato(persona(), posicion(), DESDE, HASTA, catalogo(),
                          politica(), previas, [])
    assert v.apta is False
    assert MotivoRechazo.SOBREASIGNACION in v.motivos or MotivoRechazo.CAPACIDAD in v.motivos


def test_asignacion_sin_solape_no_consume_capacidad():
    """cubre: SPEC-001/CA-01"""
    previas = [asignacion(desde=date(2026, 1, 1), hasta=date(2026, 6, 30), ded=100)]
    assert dedicacion_ocupada(previas, "PER-0001", DESDE, HASTA) == 0


def test_el_solape_se_comprueba_sobre_el_intervalo_completo_no_solo_el_inicio():
    """cubre: SPEC-001/CA-01

    El defecto clasico es comprobar solo si la fecha de inicio cae dentro del
    otro intervalo. Este caso lo detecta: la nueva empieza antes y termina
    dentro, asi que solapa aunque su inicio quede fuera.
    """
    assert solapa(date(2026, 5, 1), date(2026, 8, 15),
                  date(2026, 7, 1), date(2026, 12, 31)) is True
    assert solapa(date(2026, 1, 1), date(2026, 3, 1),
                  date(2026, 7, 1), date(2026, 12, 31)) is False


def test_sobreasignacion_dentro_de_tolerancia_exige_aprobacion_explicita():
    """cubre: SPEC-001/CA-02"""
    previas = [asignacion(ded=50, desde=DESDE, hasta=HASTA)]
    p = posicion(ded=100)  # total 150, tolerancia 25 -> fuera
    v = evaluar_candidato(persona(), p, DESDE, HASTA, catalogo(), politica(),
                          previas, [])
    assert MotivoRechazo.CAPACIDAD in v.motivos

    p2 = posicion(ded=50)  # total 100, dentro
    v2 = evaluar_candidato(persona(), p2, DESDE, HASTA, catalogo(), politica(),
                           previas, [])
    assert v2.apta is True


def test_sobreasignacion_aprobada_dentro_de_tolerancia_pasa():
    """cubre: SPEC-001/CA-02"""
    previas = [asignacion(ded=100, desde=DESDE, hasta=HASTA)]
    v = evaluar_candidato(persona(), posicion(ded=25), DESDE, HASTA, catalogo(),
                          politica(), previas, [], sobreasignacion_aprobada=True)
    assert v.apta is True


def test_sobreasignacion_no_aprobada_se_rechaza_aunque_este_en_tolerancia():
    """cubre: SPEC-001/CA-02"""
    previas = [asignacion(ded=100, desde=DESDE, hasta=HASTA)]
    v = evaluar_candidato(persona(), posicion(ded=25), DESDE, HASTA, catalogo(),
                          politica(), previas, [], sobreasignacion_aprobada=False)
    assert MotivoRechazo.SOBREASIGNACION in v.motivos


def test_categoria_por_debajo_de_la_pedida_se_rechaza():
    """cubre: SPEC-001/CA-03"""
    junior = persona(categoria="JUN")
    v = evaluar_candidato(junior, posicion(categoria="SEN"), DESDE, HASTA,
                          catalogo(), politica(), [], [])
    assert MotivoRechazo.CATEGORIA_INSUFICIENTE in v.motivos


def test_categoria_superior_a_la_pedida_es_valida():
    """cubre: SPEC-001/CA-03"""
    lead = persona(categoria="LEA")
    v = evaluar_candidato(lead, posicion(categoria="CON"), DESDE, HASTA,
                          catalogo(), politica(), [], [])
    assert v.apta is True


def test_skill_ausente_o_nivel_insuficiente_se_rechaza():
    """cubre: SPEC-001/CA-03"""
    sin_skill = persona(skills=[Skill("python", 5)])
    v = evaluar_candidato(sin_skill, posicion(skill="java", nivel=4), DESDE, HASTA,
                          catalogo(), politica(), [], [])
    assert MotivoRechazo.SKILL_AUSENTE in v.motivos

    flojo = persona(skills=[Skill("java", 2)])
    v2 = evaluar_candidato(flojo, posicion(skill="java", nivel=4), DESDE, HASTA,
                           catalogo(), politica(), [], [])
    assert MotivoRechazo.NIVEL_INSUFICIENTE in v2.motivos


def test_ausencia_aprobada_solapada_rechaza_al_candidato():
    """cubre: SPEC-001/CA-04"""
    aus = [ausencia(desde=date(2026, 8, 1), hasta=date(2026, 8, 25))]
    v = evaluar_candidato(persona(), posicion(), DESDE, HASTA, catalogo(),
                          politica(), [], aus)
    assert MotivoRechazo.AUSENCIA in v.motivos


def test_ausencia_no_aprobada_no_bloquea():
    """cubre: SPEC-001/CA-04"""
    aus = [ausencia(desde=date(2026, 8, 1), hasta=date(2026, 8, 25), aprobada=False)]
    v = evaluar_candidato(persona(), posicion(), DESDE, HASTA, catalogo(),
                          politica(), [], aus)
    assert v.apta is True


def test_persona_de_baja_antes_del_periodo_no_es_apta():
    """cubre: SPEC-001/CA-04"""
    saliente = persona(baja=date(2026, 6, 30))
    v = evaluar_candidato(saliente, posicion(), DESDE, HASTA, catalogo(),
                          politica(), [], [])
    assert MotivoRechazo.NO_ACTIVA in v.motivos


def test_la_categoria_que_cuenta_es_la_vigente_en_la_fecha_de_inicio():
    """cubre: SPEC-001/CA-05

    La persona era Consultor hasta junio y es Senior desde julio. Para una
    asignacion que empieza en marzo, la categoria que aplica es Consultor.
    """
    historico = [CategoriaVigencia("CON", date(2024, 1, 1), date(2026, 6, 30)),
                 CategoriaVigencia("SEN", date(2026, 7, 1))]
    p = persona(historico=historico)
    assert p.categoria_en(date(2026, 3, 1)) == "CON"
    assert p.categoria_en(date(2026, 9, 1)) == "SEN"


def test_una_promocion_no_reescribe_el_historico_de_asignaciones():
    """cubre: SPEC-001/CA-05"""
    historico = [CategoriaVigencia("CON", date(2024, 1, 1), date(2026, 6, 30)),
                 CategoriaVigencia("SEN", date(2026, 7, 1))]
    p = persona(historico=historico)
    a = crear_asignacion(p, posicion(categoria="CON"), "PRY-001",
                         date(2026, 3, 1), date(2026, 5, 31), catalogo(),
                         politica(), [], [], actor="test")
    assert a.categoria_registrada == "CON"
    # aunque hoy sea Senior, la asignacion pasada sigue diciendo Consultor
    assert p.categoria_en(date(2026, 9, 1)) == "SEN"
    assert a.categoria_registrada == "CON"


def test_sin_categoria_vigente_el_candidato_se_rechaza():
    """cubre: SPEC-001/CA-05"""
    historico = [CategoriaVigencia("SEN", date(2027, 1, 1))]
    p = persona(historico=historico)
    v = evaluar_candidato(p, posicion(), DESDE, HASTA, catalogo(), politica(), [], [])
    assert MotivoRechazo.SIN_CATEGORIA in v.motivos


def test_dedicacion_no_permitida_por_la_politica_se_rechaza():
    """cubre: SPEC-001/CA-06"""
    with pytest.raises(ValueError):
        crear_asignacion(persona(), posicion(ded=33), "PRY-001", DESDE, HASTA,
                         catalogo(), politica(), [], [], actor="test")


def test_dedicaciones_validas_de_la_politica_se_aceptan():
    """cubre: SPEC-001/CA-06"""
    for ded in (25, 50, 100):
        a = crear_asignacion(persona(), posicion(ded=ded), "PRY-%d" % ded,
                             DESDE, HASTA, catalogo(), politica(), [], [],
                             actor="test")
        assert a.dedicacion_pct == ded


def test_modalidad_horaria_no_exige_dedicacion_de_la_lista():
    """cubre: SPEC-001/CA-06"""
    a = crear_asignacion(persona(), posicion(ded=33), "PRY-H", DESDE, HASTA,
                         catalogo(), politica(), [], [], actor="test",
                         modalidad=Modalidad.HORARIA, horas=120)
    assert a.modalidad is Modalidad.HORARIA
    assert a.horas == 120


def test_las_demandas_se_ordenan_por_prioridad_y_luego_por_fecha():
    """cubre: SPEC-001/CA-07"""
    d = [demanda("D1", prioridad="media", momento="2026-05-01T09:00:00"),
         demanda("D2", prioridad="alta", momento="2026-05-20T09:00:00"),
         demanda("D3", prioridad="alta", momento="2026-05-02T09:00:00")]
    orden = [x.demanda_id for x in ordenar_demandas(d)]
    assert orden == ["D3", "D2", "D1"]


def test_toda_creacion_de_asignacion_escribe_traza_con_versiones(traza_temporal):
    """cubre: SPEC-001/INV-01"""
    import abaco.auditoria as auditoria
    crear_asignacion(persona(), posicion(), "PRY-001", DESDE, HASTA, catalogo(),
                     politica(), [], [], actor="resource-manager")
    entradas = auditoria.leer_traza(traza_temporal)
    assert len(entradas) == 1
    assert entradas[0]["version_catalogo"] == "CAT-2026"
    assert entradas[0]["version_politica"] == "POL-2026"
    assert entradas[0]["origen"] == "api"


def test_la_traza_registra_el_origen_agente_igual_que_el_origen_api(traza_temporal):
    """cubre: SPEC-001/INV-01

    El defecto mas peligroso del dominio es que el sistema audite lo que hacen
    las personas y deje de auditar lo que hace el agente. Las dos rutas escriben
    la misma traza.
    """
    import abaco.auditoria as auditoria
    crear_asignacion(persona(), posicion(), "PRY-001", DESDE, HASTA, catalogo(),
                     politica(), [], [], actor="agente-staffing", origen="agente")
    entradas = auditoria.leer_traza(traza_temporal)
    assert entradas[0]["origen"] == "agente"
    assert entradas[0]["version_catalogo"] == "CAT-2026"


def test_un_origen_no_declarado_se_rechaza(traza_temporal):
    """cubre: SPEC-001/INV-01"""
    from abaco.auditoria import OrigenInvalido, registrar_decision
    with pytest.raises(OrigenInvalido):
        registrar_decision("asignacion", "X", "crear", "actor", "misterioso",
                           "POL-2026", "CAT-2026", "2026-07-01T00:00:00", {})


def test_asignacion_confirmada_no_cambia_de_categoria_en_silencio():
    """cubre: SPEC-001/INV-02"""
    a = crear_asignacion(persona(), posicion(), "PRY-001", DESDE, HASTA,
                         catalogo(), politica(), [], [], actor="test")
    confirmar(a, actor="test")
    with pytest.raises(CategoriaInmutable):
        recategorizar(a, "LEA", actor="test", nueva_version_catalogo="CAT-2026")


def test_recategorizar_con_version_nueva_queda_auditado(traza_temporal):
    """cubre: SPEC-001/INV-02"""
    import abaco.auditoria as auditoria
    a = crear_asignacion(persona(), posicion(), "PRY-001", DESDE, HASTA,
                         catalogo(), politica(), [], [], actor="test")
    confirmar(a, actor="test")
    recategorizar(a, "LEA", actor="rrhh", nueva_version_catalogo="CAT-2027")
    entradas = [e for e in auditoria.leer_traza(traza_temporal)
                if e["accion"] == "recategorizar"]
    assert len(entradas) == 1
    assert entradas[0]["detalle"]["anterior"] == "SEN"
    assert entradas[0]["detalle"]["nueva"] == "LEA"


def test_el_veredicto_devuelve_todos_los_motivos_no_solo_el_primero():
    """cubre: SPEC-001/CA-03"""
    malo = persona(categoria="JUN", skills=[Skill("python", 1)])
    v = evaluar_candidato(malo, posicion(categoria="SEN", skill="java", nivel=4),
                          DESDE, HASTA, catalogo(), politica(), [], [])
    assert len(v.motivos) >= 2


def test_el_veredicto_es_reproducible_entre_ejecuciones():
    """cubre: SPEC-001/INV-03

    Los mismos datos producen el mismo veredicto y los mismos motivos, en el
    mismo orden. Sin esto no se puede defender una decision ante la persona que
    no fue propuesta, ni usar el veredicto como gate de nada.
    """
    p = persona(categoria="JUN", skills=[Skill("python", 1)])
    pos = posicion(categoria="SEN", skill="java", nivel=4)
    resultados = [evaluar_candidato(p, pos, DESDE, HASTA, catalogo(), politica(), [], [])
                  for _ in range(5)]
    assert all(r.apta == resultados[0].apta for r in resultados)
    assert all(r.motivos == resultados[0].motivos for r in resultados)


def test_el_orden_de_las_asignaciones_previas_no_altera_el_veredicto():
    """cubre: SPEC-001/INV-03"""
    previas = [asignacion(proyecto="A", desde=date(2026, 6, 1), hasta=date(2026, 9, 30), ded=50),
               asignacion(proyecto="B", desde=DESDE, hasta=HASTA, ded=50)]
    a = evaluar_candidato(persona(), posicion(ded=25), DESDE, HASTA, catalogo(),
                          politica(), previas, [])
    b = evaluar_candidato(persona(), posicion(ded=25), DESDE, HASTA, catalogo(),
                          politica(), list(reversed(previas)), [])
    assert a.apta == b.apta and a.motivos == b.motivos
