"""Dos formas de predecir el día de hoy, usando solo días que ya pasaron."""

import numpy as np
from sklearn.linear_model import LinearRegression

# Cuántos días hacia atrás mira la regresión.
DIAS_PREVIOS = 7


def prediccion_persistencia(temperaturas):
    """Baseline: hoy se predice con la temperatura de ayer."""
    return temperaturas.shift(1)


def armar_ejemplos(temperaturas, dias=DIAS_PREVIOS):
    """Cada fila de X son los días anteriores. y es el día que queremos predecir."""
    valores = temperaturas.to_numpy(dtype=float)
    entradas = []
    salidas = []
    posiciones = []
    for i in range(dias, len(valores)):
        entradas.append(valores[i - dias : i])
        salidas.append(valores[i])
        posiciones.append(i)
    return np.array(entradas), np.array(salidas), np.array(posiciones)


def entrenar_modelo(entradas, salidas):
    modelo = LinearRegression()
    modelo.fit(entradas, salidas)
    return modelo
