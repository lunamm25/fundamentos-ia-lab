"""Pasa el JSON a una tabla ordenada y la corta en entrenamiento y prueba."""

import pandas as pd


def preparar_tabla(datos):
    diario = datos["daily"]
    tabla = pd.DataFrame(
        {
            "fecha": pd.to_datetime(diario["time"]),
            "temperatura": pd.to_numeric(diario["temperature_2m_mean"]),
        }
    )
    tabla = tabla.sort_values("fecha").reset_index(drop=True)

    if tabla["fecha"].isna().any() or tabla["temperatura"].isna().any():
        raise ValueError("Hay fechas o temperaturas vacías.")

    # Cada fecha debe ser exactamente el día siguiente de la anterior.
    pasos = tabla["fecha"].diff().dropna()
    if not (pasos == pd.Timedelta(days=1)).all():
        raise ValueError("La serie no avanza de un día en uno.")
    return tabla


def cortar_serie(tabla, proporcion=0.8):
    """El primer 80 % entrena. El último 20 % se reserva para probar.

    No se mezclan las filas: el futuro no entra al entrenamiento.
    """
    corte = int(len(tabla) * proporcion)
    entrenamiento = tabla.iloc[:corte].copy()
    prueba = tabla.iloc[corte:].copy()
    return entrenamiento, prueba
