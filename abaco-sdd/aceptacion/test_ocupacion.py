"""BATERIA DE ACEPTACION EXTERNA. ESCRITA A MANO.

Esta carpeta es el unico punto de control fuera del bucle de generacion. Ningun
agente puede escribir aqui: esta en la lista de rutas denegadas del contrato de
contexto, en CODEOWNERS y en el gate de aceptacion del pipeline.

Si el agente pudiera modificar el examen que lo evalua, no habria evaluacion.

Cada test referencia el escenario de la spec que comprueba, con la etiqueta
`escenario:`, y esa referencia es lo que permite auditar que la bateria cubre
de verdad lo que dice cubrir.
"""
from datetime import date
from decimal import Decimal

from abaco.reglas.ocupacion import (capacidad_disponible, cobertura_demanda,
                                    desviacion_sobre_objetivo, dias_asignados,
                                    dias_laborables, en_banquillo,
                                    sobreasignacion, utilizacion,
                                    utilizacion_agregada)
from utilidades import (asignacion, ausencia, catalogo, demanda, persona,
                        posicion)

# Julio de 2026: 23 dias laborables
JUL_D, JUL_H = date(2026, 7, 1), date(2026, 7, 31)


def test_dias_laborables_cuenta_solo_de_lunes_a_viernes():
    """cubre: SPEC-002/CA-01"""
    assert dias_laborables(JUL_D, JUL_H) == 23
    assert dias_laborables(date(2026, 7, 4), date(2026, 7, 5)) == 0  # fin de semana


def test_utilizacion_es_asignado_entre_capacidad():
    """cubre: SPEC-002/CA-01"""
    a = [asignacion(desde=JUL_D, hasta=JUL_H, ded=100)]
    assert utilizacion(persona(), a, [], JUL_D, JUL_H) == Decimal("100.00")


def test_media_dedicacion_da_media_utilizacion():
    """cubre: SPEC-002/CA-01"""
    a = [asignacion(desde=JUL_D, hasta=JUL_H, ded=50)]
    assert utilizacion(persona(), a, [], JUL_D, JUL_H) == Decimal("50.00")


def test_sin_capacidad_disponible_devuelve_cero_sin_error():
    """cubre: SPEC-002/CA-01"""
    aus = [ausencia(tipo="vacaciones", desde=JUL_D, hasta=JUL_H)]
    assert capacidad_disponible(persona(), aus, JUL_D, JUL_H) == 0
    assert utilizacion(persona(), [], aus, JUL_D, JUL_H) == Decimal("0.00")


def test_la_formacion_y_el_banquillo_si_computan_como_capacidad():
    """cubre: SPEC-002/CA-01

    Resolucion A-01 de la ambiguedad. Excluirlos subiria la utilizacion sin
    que nadie hubiera trabajado mas, que es lo que hace el modulo heredado.
    """
    formacion = [ausencia(tipo="formacion", desde=JUL_D, hasta=JUL_H)]
    assert capacidad_disponible(persona(), formacion, JUL_D, JUL_H) == 23
    banquillo = [ausencia(tipo="banquillo", desde=JUL_D, hasta=JUL_H)]
    assert capacidad_disponible(persona(), banquillo, JUL_D, JUL_H) == 23


def test_vacaciones_festivo_y_baja_no_computan_como_capacidad():
    """cubre: SPEC-002/CA-01"""
    for tipo in ("vacaciones", "festivo", "baja"):
        aus = [ausencia(tipo=tipo, desde=date(2026, 7, 6), hasta=date(2026, 7, 10))]
        assert capacidad_disponible(persona(), aus, JUL_D, JUL_H) == 18, tipo


def test_la_utilizacion_se_compara_contra_el_objetivo_de_su_categoria():
    """cubre: SPEC-002/CA-02"""
    a = [asignacion(desde=JUL_D, hasta=JUL_H, ded=100)]
    senior = persona(categoria="SEN")     # objetivo 85
    director = persona(pid="PER-0002", categoria="DIR")  # objetivo 35
    a2 = [asignacion(pid="PER-0002", desde=JUL_D, hasta=JUL_H, ded=100)]
    assert desviacion_sobre_objetivo(senior, catalogo(), a, [], JUL_D, JUL_H) == Decimal("15.00")
    assert desviacion_sobre_objetivo(director, catalogo(), a2, [], JUL_D, JUL_H) == Decimal("65.00")


def test_el_mismo_numero_es_bueno_o_malo_segun_la_categoria():
    """cubre: SPEC-002/CA-02

    Un 60% de utilizacion esta por debajo del objetivo de un Senior y muy por
    encima del de un Director. Un objetivo unico de compania no vale.
    """
    a = [asignacion(desde=JUL_D, hasta=JUL_H, ded=50), 
         asignacion(desde=JUL_D, hasta=date(2026, 7, 15), ded=25)]
    senior = persona(categoria="SEN")
    d_sen = desviacion_sobre_objetivo(senior, catalogo(), a, [], JUL_D, JUL_H)
    assert d_sen < 0
    director = persona(pid="PER-0002", categoria="DIR")
    a2 = [asignacion(pid="PER-0002", desde=JUL_D, hasta=JUL_H, ded=50)]
    assert desviacion_sobre_objetivo(director, catalogo(), a2, [], JUL_D, JUL_H) > 0


def test_el_prorrateo_es_por_dias_laborables_efectivos_del_solape():
    """cubre: SPEC-002/CA-03

    Una asignacion que cubre media parte del mes aporta la mitad, no el mes
    entero ni una proporcion sobre dias naturales.
    """
    a = [asignacion(desde=date(2026, 7, 1), hasta=date(2026, 7, 17), ded=100)]
    # del 1 al 17 de julio de 2026 hay 13 dias laborables de 23
    assert dias_asignados("PER-0001", a, JUL_D, JUL_H) == Decimal("13")
    esperado = (Decimal("13") / Decimal("23") * 100).quantize(Decimal("0.01"))
    assert utilizacion(persona(), a, [], JUL_D, JUL_H) == esperado


def test_asignacion_que_empieza_antes_del_periodo_solo_cuenta_el_solape():
    """cubre: SPEC-002/CA-03"""
    a = [asignacion(desde=date(2026, 5, 1), hasta=date(2026, 7, 10), ded=100)]
    assert dias_asignados("PER-0001", a, JUL_D, JUL_H) == Decimal("8")


def test_cobertura_de_demanda_por_categoria_igual_o_superior():
    """cubre: SPEC-002/CA-04"""
    d = demanda(posiciones=[posicion(rol="desarrollo", categoria="CON"),
                            posicion(rol="arquitectura", categoria="SEN")])
    a = [asignacion(rol="desarrollo", categoria="SEN", proyecto="PRY-001")]
    assert cobertura_demanda(d, a, {}, catalogo()) == Decimal("50.00")


def test_una_categoria_inferior_no_cubre_la_posicion():
    """cubre: SPEC-002/CA-04"""
    d = demanda(posiciones=[posicion(rol="desarrollo", categoria="SEN")])
    a = [asignacion(rol="desarrollo", categoria="JUN", proyecto="PRY-001")]
    assert cobertura_demanda(d, a, {}, catalogo()) == Decimal("0.00")


def test_la_sobreasignacion_se_corta_en_100_en_la_utilizacion():
    """cubre: SPEC-002/CA-05

    Resolucion A-02 de la ambiguedad. Una persona al 150% no tiene una
    utilizacion del 150%: tiene un 100% y un problema.
    """
    a = [asignacion(proyecto="A", desde=JUL_D, hasta=JUL_H, ded=100),
         asignacion(proyecto="B", desde=JUL_D, hasta=JUL_H, ded=50)]
    assert utilizacion(persona(), a, [], JUL_D, JUL_H) == Decimal("100.00")


def test_sin_cortar_el_calculo_daria_150_y_por_eso_se_corta():
    """cubre: SPEC-002/CA-05"""
    a = [asignacion(proyecto="A", desde=JUL_D, hasta=JUL_H, ded=100),
         asignacion(proyecto="B", desde=JUL_D, hasta=JUL_H, ded=50)]
    sin_cortar = dias_asignados("PER-0001", a, JUL_D, JUL_H, cortar_en_100=False)
    assert sin_cortar == Decimal("34.5")


def test_la_sobreasignacion_se_reporta_como_indicador_propio():
    """cubre: SPEC-002/CA-06"""
    a = [asignacion(proyecto="A", desde=JUL_D, hasta=JUL_H, ded=100),
         asignacion(proyecto="B", desde=JUL_D, hasta=JUL_H, ded=50)]
    assert sobreasignacion(persona(), a, JUL_D, JUL_H) == Decimal("50.00")
    assert utilizacion(persona(), a, [], JUL_D, JUL_H) == Decimal("100.00")


def test_sin_exceso_la_sobreasignacion_es_cero():
    """cubre: SPEC-002/CA-06"""
    a = [asignacion(desde=JUL_D, hasta=JUL_H, ded=100)]
    assert sobreasignacion(persona(), a, JUL_D, JUL_H) == Decimal("0.00")


def test_el_agregado_suma_numerador_y_denominador_y_redondea_una_vez():
    """cubre: SPEC-002/INV-01

    Caso elegido para que promediar utilizaciones individuales de un resultado
    distinto de agregar. Una persona con mucha capacidad y poca ocupacion pesa
    mas en el agregado correcto que en la media de porcentajes.
    """
    p1 = persona(pid="PER-0001")
    p2 = persona(pid="PER-0002")
    aus = [ausencia(pid="PER-0002", tipo="vacaciones",
                    desde=date(2026, 7, 6), hasta=date(2026, 7, 24))]
    a = [asignacion(pid="PER-0001", desde=JUL_D, hasta=JUL_H, ded=50),
         asignacion(pid="PER-0002", desde=JUL_D, hasta=JUL_H, ded=100)]
    agregada = utilizacion_agregada([p1, p2], a, aus, JUL_D, JUL_H)
    media_de_porcentajes = (
        (utilizacion(p1, a, aus, JUL_D, JUL_H) + utilizacion(p2, a, aus, JUL_D, JUL_H))
        / 2).quantize(Decimal("0.01"))
    assert agregada != media_de_porcentajes
    # numerador: 11.5 + 8 = 19.5 ; denominador: 23 + 8 = 31
    assert agregada == (Decimal("19.5") / Decimal("31") * 100).quantize(Decimal("0.01"))


def test_el_agregado_incluye_a_la_gente_en_banquillo():
    """cubre: SPEC-002/INV-01

    Es la diferencia que mas mueve el numero de compania frente al modulo
    heredado, que excluye al banquillo entero del calculo.
    """
    ocupada = persona(pid="PER-0001")
    banquillo = persona(pid="PER-0002")
    a = [asignacion(pid="PER-0001", desde=JUL_D, hasta=JUL_H, ded=100)]
    con_banquillo = utilizacion_agregada([ocupada, banquillo], a, [], JUL_D, JUL_H)
    sin_banquillo = utilizacion_agregada([ocupada], a, [], JUL_D, JUL_H)
    assert con_banquillo == Decimal("50.00")
    assert sin_banquillo == Decimal("100.00")


def test_aritmetica_decimal_no_coma_flotante():
    """cubre: SPEC-002/INV-02"""
    a = [asignacion(desde=JUL_D, hasta=date(2026, 7, 10), ded=25)]
    r = utilizacion(persona(), a, [], JUL_D, JUL_H)
    assert isinstance(r, Decimal)


def test_el_orden_de_las_asignaciones_no_altera_el_resultado():
    """cubre: SPEC-002/INV-03"""
    a = [asignacion(proyecto="A", desde=JUL_D, hasta=date(2026, 7, 15), ded=50),
         asignacion(proyecto="B", desde=date(2026, 7, 16), hasta=JUL_H, ded=25)]
    assert (utilizacion(persona(), a, [], JUL_D, JUL_H)
            == utilizacion(persona(), list(reversed(a)), [], JUL_D, JUL_H))


def test_una_asignacion_no_computa_durante_una_ausencia_no_trabajable():
    """cubre: SPEC-002/CA-08

    Alguien asignado al 100% que esta tres semanas de vacaciones no ha
    trabajado esas tres semanas. Si el numerador las cuenta y el denominador
    no, la utilizacion se dispara por encima del 100% sin que nadie haya hecho
    nada. Numerador y denominador excluyen exactamente los mismos dias.
    """
    a = [asignacion(desde=JUL_D, hasta=JUL_H, ded=100)]
    aus = [ausencia(tipo="vacaciones", desde=date(2026, 7, 6), hasta=date(2026, 7, 24))]
    assert capacidad_disponible(persona(), aus, JUL_D, JUL_H) == 8
    assert dias_asignados("PER-0001", a, JUL_D, JUL_H, aus) == Decimal("8")
    assert utilizacion(persona(), a, aus, JUL_D, JUL_H) == Decimal("100.00")


def test_deteccion_de_banquillo():
    """cubre: SPEC-002/CA-07"""
    assert en_banquillo(persona(), [], [], JUL_D, JUL_H) is True
    a = [asignacion(desde=JUL_D, hasta=JUL_H, ded=25)]
    assert en_banquillo(persona(), a, [], JUL_D, JUL_H) is False


def test_sin_capacidad_no_se_considera_banquillo():
    """cubre: SPEC-002/CA-07"""
    aus = [ausencia(tipo="vacaciones", desde=JUL_D, hasta=JUL_H)]
    assert en_banquillo(persona(), [], aus, JUL_D, JUL_H) is False
