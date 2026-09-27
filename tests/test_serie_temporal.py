"""Tres pruebas: orden, datos vacíos y el corte temporal."""

import pandas as pd
import pytest

from serie_temporal.evaluation import mae, rmse
from serie_temporal.preprocessing import cortar_serie, preparar_tabla


def test_ordena_las_fechas_y_no_deja_vacios():
    datos = {
        "daily": {
            "time": ["2024-01-03", "2024-01-01", "2024-01-02"],
            "temperature_2m_mean": [14, 10, 12],
        }
    }
    tabla = preparar_tabla(datos)
    assert tabla["temperatura"].isna().sum() == 0
    assert list(tabla["fecha"].dt.strftime("%Y-%m-%d")) == [
        "2024-01-01",
        "2024-01-02",
        "2024-01-03",
    ]


def test_avisa_si_falta_un_dato():
    datos = {
        "daily": {
            "time": ["2024-01-01", "2024-01-02"],
            "temperature_2m_mean": [10, None],
        }
    }
    with pytest.raises(ValueError):
        preparar_tabla(datos)


def test_el_corte_deja_el_futuro_al_final():
    tabla = pd.DataFrame(
        {
            "fecha": pd.date_range("2024-01-01", periods=10, freq="D"),
            "temperatura": range(10),
        }
    )
    entrenamiento, prueba = cortar_serie(tabla)
    assert len(entrenamiento) == 8
    assert len(prueba) == 2
    assert entrenamiento["fecha"].max() < prueba["fecha"].min()


def test_mae_y_rmse():
    assert mae([1, 2], [1, 2]) == 0
    assert mae([3, 5], [1, 1]) == 3
    assert rmse([0, 0], [0, 0]) == 0
