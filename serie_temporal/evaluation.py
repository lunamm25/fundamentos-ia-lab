"""MAE y RMSE. Los dos se miden en grados Celsius."""

import numpy as np


def mae(real, prediccion):
    """Promedio de |real - predicción|."""
    real = np.asarray(real, dtype=float)
    prediccion = np.asarray(prediccion, dtype=float)
    return float(np.mean(np.abs(real - prediccion)))


def rmse(real, prediccion):
    """Raíz del promedio de los errores al cuadrado. Castiga más los errores grandes."""
    real = np.asarray(real, dtype=float)
    prediccion = np.asarray(prediccion, dtype=float)
    return float(np.sqrt(np.mean((real - prediccion) ** 2)))
