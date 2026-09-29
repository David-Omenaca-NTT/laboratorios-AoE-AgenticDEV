import importlib.util
from pathlib import Path

import pytest


RAIZ = Path(__file__).resolve().parents[1]
RUTA_VERIFICADOR = RAIZ / "labs" / "S0-bootstrap" / "verificar.py"
ESPECIFICACION = importlib.util.spec_from_file_location("verificar_s0", RUTA_VERIFICADOR)
VERIFICADOR = importlib.util.module_from_spec(ESPECIFICACION)
ESPECIFICACION.loader.exec_module(VERIFICADOR)


@pytest.mark.parametrize(
    "resultado",
    VERIFICADOR.verificar(),
    ids=lambda resultado: resultado["id"],
)
def test_criterios_de_s0(resultado):
    """Cubre los criterios S0-01 a S0-05."""
    assert resultado["ok"], resultado["detalle"]