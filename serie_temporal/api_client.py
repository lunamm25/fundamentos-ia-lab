"""Pide la temperatura diaria a Open-Meteo. No hace falta API key."""

import requests

URL = "https://archive-api.open-meteo.com/v1/archive"
PARAMETROS = {
    "latitude": 5.07,
    "longitude": -75.52,
    "start_date": "2024-01-01",
    "end_date": "2025-12-31",
    "daily": "temperature_2m_mean",
    "timezone": "America/Bogota",
}


def obtener_datos():
    respuesta = requests.get(URL, params=PARAMETROS, timeout=60)
    respuesta.raise_for_status()
    return respuesta.json()
